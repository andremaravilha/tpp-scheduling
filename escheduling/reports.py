from datetime import datetime
import locale
from mailmerge import MailMerge


def schedule_to_doc(output, template, data, schedule, lang='pt_BR'):

    # Set locale
    locale.setlocale(locale.LC_TIME, lang)

    # Get data to write the schedule file
    rows = []
    for entry in schedule:
        
        authors = sorted(data['works'][entry['work']]['authors'])
        evaluators = sorted([data['evaluators'][idx]['name'] for idx in entry['evaluators']])

        dt = datetime.fromisoformat('{}T{}'.format(
            data['datetimes'][entry['datetime']]['date'],
            data['datetimes'][entry['datetime']]['start']))

        rows.append({
            'datetime': dt,
            'date': dt.strftime('%x\n%A'), 
            'time': dt.strftime('%Hh%M'), 
            'room': data['rooms'][entry['room']]['description'], 
            'work': data['works'][entry['work']]['title'], 
            'authors': '\n '.join(authors), 
            'evaluators': '\n '.join(evaluators)
        })

    # Sort rows by datetime field
    rows.sort(key=lambda entry: entry['datetime'])

    # Load and fill template file
    document = MailMerge(template)
    document.merge_rows('date', rows)

    # Export output file
    document.write(output)

