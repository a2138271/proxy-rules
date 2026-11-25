from pathlib import Path
import yaml

root = Path(__file__).resolve().parent
groups = [('openai', '🤖 OpenAI'), ('proxy', 'PROXY'), ('direct', 'DIRECT')]
lines = ['# Generated from clash-*.yaml', '[Proxy Group]',
         '🤖 OpenAI = select, policy-regex-filter=^other$', '', '[Rule]']
seen = {}
for name, policy in groups:
    rules = yaml.safe_load((root / f'clash-{name}.yaml').read_text())['payload']
    for rule in rules:
        kind, value, *options = rule.split(',')
        if options not in ([], ['no-resolve']):
            raise ValueError(f'Unexpected rule options: {rule}')
        if rule in seen:
            if seen[rule] != policy:
                raise ValueError(f'Conflicting policies for {rule}')
            continue
        seen[rule] = policy
        lines.append(','.join([kind, value, policy, *options]))
lines.extend(['GEOIP,CN,DIRECT', 'FINAL,PROXY'])
(root / 'shadowrocket.conf').write_text('\n'.join(lines) + '\n')
