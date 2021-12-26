import altair as alt


def build_map(world, data, lookup_field, scale, legend_title, field_type='Q'):
    return alt.Chart(world, width=900, height=600).transform_lookup(
        lookup='name',
        from_=alt.LookupData(data=data, key='country', fields=['country', lookup_field]),
        default='0',
    ).project('equalEarth').mark_geoshape().encode(
        color=alt.Color(f'{lookup_field}:{field_type}', scale=scale, legend=alt.Legend(title=legend_title)),
        tooltip=[alt.Tooltip('name:N'), alt.Tooltip(f'{lookup_field}:{field_type}')],
    )


def build_map_2(world, data):
    selection = alt.selection_single(fields=['country'], on='mouseover', empty='all')
    world_map = alt.Chart(world, height=400, width=600).transform_lookup(
        lookup='name',
        from_=alt.LookupData(data=data, key='country', fields=['country', 'Self-harm']),
        default='0',
    ).project('equalEarth').mark_geoshape().encode(
        color=alt.Color(f'Self-harm:Q', scale=alt.Scale(scheme='reds')),
        tooltip=[alt.Tooltip('name:N')],
    ).add_selection(selection)

    bars = alt.Chart(data, height=400, width=600).mark_bar().encode(
        x=alt.X('Year:Q'),
        y=alt.Y('Self-harm:Q'),
    ).transform_filter(selection)

    return world_map | bars


def build_bar(data):
    return alt.Chart(data, height=600, width=1000).mark_bar(opacity=0.8).encode(
        x=alt.X('deaths:Q', stack=None),
        y=alt.Y('category:N', sort='-x'),
    )


def build_bar_2(data):
    return alt.Chart(data, height=600, width=1000).mark_bar(opacity=0.6).encode(
        x=alt.X('deaths:Q', stack=None),
        y=alt.Y('category:N', sort='-x'),
        color=alt.Color('mark:N', scale=alt.Scale(scheme='set1'), legend=alt.Legend(title='Death number')),
    )


def build_lines(data):
    return alt.Chart(data, height=400, width=600).mark_line().encode(
        x=alt.X('Year:O'),
        y=alt.Y('deaths:Q'),
        color=alt.Color('category:N', scale=alt.Scale(scheme='set1'), legend=alt.Legend(title='Death causes')),
    )


def build_lines_2(data):
    input_dropdown = alt.binding_select(options=['Maternal disorders', 'Neonatal disorders'], name='Disorders')
    selection = alt.selection_single(fields=['category'], bind=input_dropdown, empty='all')
    return alt.Chart(data, height=500, width=800).mark_line().encode(
        x=alt.X('Year:O'),
        y=alt.Y('deaths:Q'),
        color=alt.Color('country:N', scale=alt.Scale(scheme='set1')),
    ).add_selection(selection).transform_filter(selection)


def add_title(chart, title):
    return chart.properties(
        title=title,
    ).configure_title(
        fontSize=24,
        font='Courier',
        anchor='middle',
        dy=-30
    )
