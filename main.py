from source import *
from chart_builder import *
import altair as alt


def task1():
    world_map = load_map()
    summary = get_death_summary_by_country()

    chart = build_map(world=world_map,
                      data=summary,
                      lookup_field='deaths',
                      legend_title='Deaths',
                      scale=alt.Scale(scheme='reds'))

    return add_title(chart, 'Number of deaths during 1990-2017')


def task2():
    world_map = load_map()
    compare_data = get_deaths_comparison(get_mean_deaths_by_country(),
                                         get_last_year_death_summary_by_country(),
                                         on='country').round()

    chart = build_map(world=world_map,
                      data=compare_data,
                      lookup_field='deaths_change',
                      legend_title='Death change',
                      scale=alt.Scale(domainMid=0, scheme='redblue', reverse=True))
    return add_title(chart, 'Number of deaths in 2017 comparing with 27 years average value')


def task3():
    category_summary = get_deaths_summary_by_category()
    chart = build_bar(category_summary)
    return add_title(chart, 'Quantitative distribution of causes of death')


def task4():
    compare_data = get_deaths_mean_by_category().append(get_deaths_for_last_year_by_category())
    chart = build_bar_2(compare_data)
    return add_title(
        chart,
        'Change of quantitative distribution of death causes in 2017 comparing with 27 years average value',
    )


def task5():
    crisis_data = get_deaths_summary_for_2008_crisis()
    chart = build_lines(crisis_data)
    return add_title(chart, '2008 crisis and its influence on selected causes of death in USA')


def task6_1():
    crisis_data = get_deaths_summary_for_maternal_and_neonatal_g6()
    chart = build_lines_2(crisis_data)
    return add_title(chart, 'Maternal/Neonatal disorders progress in top 6 countries')


def tas6_2():
    crisis_data_2 = get_deaths_summary_for_maternal_and_neonatal_bad_countries()
    chart = build_lines_2(crisis_data_2)
    return add_title(chart, 'Maternal/Neonatal disorders progress in 6 third world countries')


def task7():
    disease_data = get_disease_deaths_summary_in_america()
    chart = build_lines(disease_data)
    return add_title(chart, 'Diseases progress in USA')


def task8():
    world_map = load_map()
    suicide = get_suicide_analysis()
    chart = build_map_2(world=world_map, data=suicide)

    return add_title(chart, 'Suicide progress in countries')


if __name__ == '__main__':
    alt.data_transformers.disable_max_rows()
    task8().show()
