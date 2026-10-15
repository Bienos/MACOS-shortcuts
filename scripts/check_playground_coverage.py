#!/usr/bin/env python3
"""Validate that every imported workbook row has a known playground mapping."""
import json
from collections import Counter
from pathlib import Path

APP = Path(__file__).resolve().parents[1]
DATA = APP / 'data' / 'shortcuts.json'
ALLOWED = {'text', 'files', 'windows', 'browser', 'capture', 'code', 'app', 'guided'}
data = json.loads(DATA.read_text(encoding='utf-8'))
records = data['records']
unmapped = [r for r in records if r.get('playgroundType') not in ALLOWED or not r.get('playgroundReason')]
ambiguous = [{'id': r['id'], 'reason': r.get('playgroundReason', '')} for r in records if r.get('playgroundType') == 'guided']
report = {
    'sourceWorkbook': data['sourceWorkbook'],
    'sourceSheet': data['sourceSheet'],
    'totalWorkbookRecordsImported': data['recordCount'],
    'recordsInJson': len(records),
    'mappedRecords': len(records) - len(unmapped),
    'byPlaygroundType': dict(sorted(Counter(r.get('playgroundType') for r in records).items())),
    'unmapped': [{'id': r['id'], 'reason': 'Brak rozpoznanego szablonu lub uzasadnienia mapowania.'} for r in unmapped],
    'guidedVisualizationRecords': ambiguous,
}
(APP / 'data' / 'playground-coverage.json').write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
print(f"Workbook rows imported: {report['totalWorkbookRecordsImported']}")
print(f"Mapped to playground template: {report['mappedRecords']}/{report['recordsInJson']}")
print('Counts by template: ' + ', '.join(f'{k}={v}' for k, v in report['byPlaygroundType'].items()))
print(f"Guided visualizations (explicitly documented): {len(ambiguous)}; IDs and reasons in data/playground-coverage.json")
if unmapped:
    print('UNMAPPED:')
    for row in report['unmapped']:
        print(f"  {row['id']}: {row['reason']}")
    raise SystemExit(1)
