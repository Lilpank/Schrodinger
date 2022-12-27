import dearpygui.dearpygui as dpg
import utilities
import numpy as np

DEFAULT_VALUE_BTN_N = 100
DEFAULT_VALUE_BTN_X_MIN = 0
DEFAULT_VALUE_BTN_X_MAX = 10

DEFAULT_VALUE_BTN_ACCURACY = -5
DEFAULT_VALUE_BTN_B = 10
DEFAULT_VALUE_BTN_E_MIN = -0.5
DEFAULT_VALUE_BTN_E_MAX = 1
DEFAULT_VALUE_BTN_H_ENERGY = 10 ** (-4)

dpg.create_context()

WIDTH = 1300
HEIGHT = 900

plt_potential_F = []

plt_psi_tag = []
plt_E_tag = []

vector_x, h = np.linspace(DEFAULT_VALUE_BTN_X_MIN, DEFAULT_VALUE_BTN_X_MAX, DEFAULT_VALUE_BTN_N, retstep=True)
value_potential = utilities.u_potential(vector_x)
psi, energy, m = utilities.find_vector_value(DEFAULT_VALUE_BTN_E_MIN, DEFAULT_VALUE_BTN_E_MAX,
                                             DEFAULT_VALUE_BTN_H_ENERGY,
                                             5 * 10 ** DEFAULT_VALUE_BTN_ACCURACY, DEFAULT_VALUE_BTN_B, value_potential,
                                             DEFAULT_VALUE_BTN_N, h)

table_id = 0


def clear_table(energy):
    for tag in dpg.get_item_children(table_id)[1]:
        dpg.delete_item(tag)
    for i in range(0, len(energy)):
        with dpg.table_row(parent=table_id, tag=f'row_{i}'):
            dpg.add_text(f"  {i}     {format(energy[i], '.4f')}    {format(vector_x[int(m[i])], '.4f')}")


with dpg.window(label="n,    E,         x", pos=(0, round(HEIGHT / 2) - 13)):
    table_id = dpg.generate_uuid()
    with dpg.table(header_row=False, width=round(WIDTH / 4) - 18, height=round(HEIGHT / 2) - 80, tag=table_id):
        dpg.add_table_column()
        dpg.add_table_column()

        for i in range(0, len(energy)):
            with dpg.table_row(parent=table_id, tag=f'row_{i}'):
                dpg.add_text(f"  {i}     {format(energy[i], '.4f')}    {format(vector_x[int(m[i])], '.4f')}")


def find_vector():
    global x_max, x_min, vector_x, h, plt_potential_F, plt_psi_tag, m
    x_min = int(dpg.get_value(btn_x_min))
    x_max = int(dpg.get_value(btn_x_max))
    n = int(dpg.get_value(btn_N))

    vector_x, h = np.linspace(x_min, x_max, n, retstep=True)
    value_potential = utilities.f_potential(vector_x)

    for i in plt_potential_F:
        dpg.set_value(i, [vector_x, value_potential])

    e_min = dpg.get_value(btn_e_min)
    e_max = dpg.get_value(btn_e_max)
    h_energy = dpg.get_value(btn_h_energy)
    accuracy = 5 * 10 ** dpg.get_value(btn_accuracy)
    b_coefficient = dpg.get_value(btn_B)
    n = int(dpg.get_value(btn_N))

    try:
        psi, energy, m = utilities.find_vector_value(e_min, e_max, h_energy, accuracy, b_coefficient, value_potential,
                                                     n, h)
    except:
        return

    while len(plt_psi_tag) != 0:
        dpg.delete_item(plt_psi_tag.pop())
        dpg.delete_item(plt_E_tag.pop())

    energy = np.flip(energy)

    z = 0
    for i in psi:
        tag = dpg.generate_uuid()
        plt_psi_tag.append(tag)
        dpg.add_line_series(vector_x, i, label=f"n={z}", parent="y_axis1", tag=tag)
        z += 1

    z = 0
    for i in psi:
        tag = dpg.generate_uuid()
        plt_E_tag.append(tag)
        dpg.add_line_series(vector_x, [energy[z] for j in range(dpg.get_value(btn_N))], label=f"E=%.4f" % energy[z],
                            parent="y_axis2", tag=tag)
        z += 1

    clear_table(energy)


with dpg.window(label="Schrodinger params", pos=(0, 0), height=round((HEIGHT / 2) - 15),
                width=round(WIDTH / 4) - 2) as win:
    btn_x_min = dpg.add_input_double(label="x_min", enabled=True, default_value=DEFAULT_VALUE_BTN_X_MIN, step=1)
    btn_x_max = dpg.add_input_double(label="x_max", enabled=True, default_value=DEFAULT_VALUE_BTN_X_MAX, step=1)
    btn_N = dpg.add_input_int(label="N", enabled=True, default_value=DEFAULT_VALUE_BTN_N, step=1)

    btn_accuracy = dpg.add_input_int(label="eps 10^(-x)", enabled=True, default_value=DEFAULT_VALUE_BTN_ACCURACY,
                                     step=1)
    btn_B = dpg.add_input_double(label="B=2ma²Uo/h²", enabled=True, default_value=DEFAULT_VALUE_BTN_B,
                                 step=1)
    btn_e_min = dpg.add_input_double(label="E_min", enabled=True, default_value=DEFAULT_VALUE_BTN_E_MIN, step=0.1)
    btn_e_max = dpg.add_input_double(label="E_max", enabled=True, default_value=DEFAULT_VALUE_BTN_E_MAX, step=0.1)
    btn_h_energy = dpg.add_input_double(label="h_energy", enabled=True, default_value=DEFAULT_VALUE_BTN_H_ENERGY,
                                        step=0.1,
                                        format="%.4f")

    dpg.set_item_callback(btn_x_min, find_vector)
    dpg.set_item_callback(btn_x_max, find_vector)
    dpg.set_item_callback(btn_N, find_vector)
    dpg.set_item_callback(btn_accuracy, find_vector)
    dpg.set_item_callback(btn_B, find_vector)
    dpg.set_item_callback(btn_e_min, find_vector)
    dpg.set_item_callback(btn_e_max, find_vector)
    dpg.set_item_callback(btn_h_energy, find_vector)

with dpg.window(label="PLOT", tag="win", pos=(round(WIDTH / 4), 0), width=round(WIDTH - 90)):
    with dpg.plot(label="plt1", height=round(HEIGHT / 2 - 50), width=round(WIDTH - 100), anti_aliased=True,
                  no_title=True):
        dpg.add_plot_legend()
        dpg.add_plot_axis(dpg.mvXAxis, label="X", tag="x_axis1")
        dpg.add_plot_axis(dpg.mvYAxis, label="U(x) | Psi(x)", tag="y_axis1")

        plt_potential_F.append(dpg.generate_uuid())
        dpg.add_line_series(vector_x, value_potential, label="F(x) = -1 / (exp(x - 5) + 1)", parent="y_axis1",
                            tag=plt_potential_F[0])

        z = 0
        for i in psi:
            tag = dpg.generate_uuid()
            plt_psi_tag.append(tag)
            dpg.add_line_series(vector_x, i, label=f"n={z}", parent="y_axis1", tag=tag)
            z += 1
    with dpg.plot(label="plt2", height=round(HEIGHT / 2 - 50), width=round(WIDTH - 100), anti_aliased=True,
                  no_title=True):
        dpg.add_plot_legend()
        dpg.add_plot_axis(dpg.mvXAxis, label="x", tag="x_axis2")
        dpg.add_plot_axis(dpg.mvYAxis, label="U(x)", tag="y_axis2")

        plt_potential_F.append(dpg.generate_uuid())
        dpg.add_line_series(vector_x, value_potential, label="F(x) = -1 / (exp(x - 5) + 1)", parent="y_axis2",
                            tag=plt_potential_F[1])
        z = 0
        for i in psi:
            tag = dpg.generate_uuid()
            plt_E_tag.append(tag)
            dpg.add_line_series(vector_x, [energy[z] for j in range(dpg.get_value(btn_N))], label=f"E=%.4f" % energy[z],
                                parent="y_axis2", tag=tag)
            z += 1

dpg.create_viewport(title='Schrodinger equation', width=WIDTH, height=HEIGHT)
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()
