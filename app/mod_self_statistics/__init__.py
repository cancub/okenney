import datetime as _datetime
import re as _re

import app.mod_self_statistics.models as _models

SELF_STATISTICS_PATH = '/consumption-data'

DEFAULT_QUANTITY_UNITS = {
    'beer': 'mL',
    'wine': 'mL',
    'spirit': 'fl oz',
    'cannabis': 'toke',
    'chips': 'g',
    'cigarette': 'cigarette',
    'coffee': 'mL',
}

def _translate_quantity(consom):
    # Figure out what unit we'd like the output to be in.
    target_unit = DEFAULT_QUANTITY_UNITS[consom.category]

    if consom.unit.startswith(target_unit):
        return consom.quantity

    target_unit_quant = float(
        _re.search(rf'\(([\d\.]+) {target_unit}\)', consom.unit).group(1)
    )
    return target_unit_quant * float(consom.quantity)

def get_chart_data():
    '''
    Build a day-by-day breakdown of consumption for each category.
    '''
    categories = [c.name for c in _models.Category.query.all()]
    data = {c: {} for c in categories}

    # Keep track of the earliest date we've seen.
    now = _datetime.datetime.now().date()
    min_date = now

    # Also keep track of the maximum value we've seen for each category.
    maximums = {c: 0.1 for c in categories}

    # Collect all of the data
    for c in _models.Consumption.query.all():
        category = c.category
        date = c.datetime.date()
        quantity = _translate_quantity(c)

        min_date = min(min_date, date)

        try:
            data[category][str(date)] += quantity
        except KeyError:
            data[category][str(date)] = quantity

        maximums[category] = max(maximums[category], data[category][str(date)])

    # Now walk through the data and fill in the blanks with zeros.
    dates = [
        str(min_date + _datetime.timedelta(days=d))
        for d in range((now-min_date).days + 1)
    ]
    for date in dates:
        for cat, cat_data in data.items():
            if str(date) not in cat_data:
                cat_data[str(date)] = 0

    # Finally, reformat the data so that it is a list of dicts.
    data_list = []
    for cat, cat_data in data.items():
        for date, value in cat_data.items():
            data_list.append({'category': cat, 'date': date, 'value': value})

    return {
        'data': data_list,
        'categories': categories,
        'dates': dates,
        'maximums': maximums,
        'units': DEFAULT_QUANTITY_UNITS,
    }
