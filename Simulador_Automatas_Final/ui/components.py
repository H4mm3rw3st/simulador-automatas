import flet as ft

def tabla_transiciones(trans):
    rows = []
    for (o, s), d in trans.items():
        rows.append(
            ft.DataRow(cells=[
                ft.DataCell(ft.Text(str(o))),
                ft.DataCell(ft.Text(s)),
                ft.DataCell(ft.Text(str(d)))
            ])
        )

    return ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("Origen")),
            ft.DataColumn(ft.Text("Símbolo")),
            ft.DataColumn(ft.Text("Destino")),
        ],
        rows=rows
    )