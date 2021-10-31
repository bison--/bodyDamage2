import dearpygui.dearpygui as dpg
import BodyDamageHandler


def save_callback(sender, app_dat):
    print("Save Clicked", sender, app_dat)


def move_window(sender, app_dat):
    print("move_window:", sender, app_dat, dpg.get_item_pos(dpg.get_item_parent(sender)))


WINDOW_SIZE = (670, 712)

bd_handler = BodyDamageHandler.BodyDamageHandler()

dpg.create_context()
dpg.create_viewport()
dpg.setup_dearpygui()

dpg.set_viewport_title("Body Damage Calculator v2")
dpg.set_viewport_width(WINDOW_SIZE[0])
dpg.set_viewport_height(WINDOW_SIZE[1])
dpg.set_viewport_max_width(WINDOW_SIZE[0])
dpg.set_viewport_max_height(WINDOW_SIZE[1])
dpg.set_viewport_min_width(WINDOW_SIZE[0])
dpg.set_viewport_min_height(WINDOW_SIZE[1])

# TODO: make icons
#dpg.set_viewport_small_icon()


# load image
width, height, channels, data = dpg.load_image("vitruvianMan.png")
with dpg.texture_registry(show=False):
    dpg.add_static_texture(width, height, data, tag="vitruvianMan")

with dpg.window(tag='mainWindow', label="Body Damage Calculator v2", min_size=WINDOW_SIZE, max_size=WINDOW_SIZE):
    dpg.add_image('vitruvianMan', pos=(140, 80), width=381, height=401)

    # body parts
    dpg.add_slider_int(tag='sldHead', label="HEAD", pos=(270, 60), width=100, default_value=100, callback=bd_handler.calculate)
    dpg.add_slider_int(tag='sldUBody', label="U. Body", pos=(100, 230), width=100, default_value=100, callback=bd_handler.calculate)
    dpg.add_slider_int(tag='sldLBody', label="L. Body", pos=(100, 280), width=100, default_value=100, callback=bd_handler.calculate)

    dpg.add_slider_int(tag='sldRArm', label="R. ARM", pos=(69, 120), width=100, default_value=100, callback=bd_handler.calculate)
    dpg.add_slider_int(tag='sldRHand', label="R. HAND", pos=(10, 160), width=100, default_value=100, callback=bd_handler.calculate)

    dpg.add_slider_int(tag='sldRLeg', label="R. LEG", pos=(10, 360), width=100, default_value=100, callback=bd_handler.calculate)
    dpg.add_slider_int(tag='sldRFeet', label="R. FEET", pos=(171, 490), width=100, default_value=100, callback=bd_handler.calculate)

    dpg.add_slider_int(tag='sldLArm', label="L. ARM", pos=(449, 120), width=100, default_value=100, callback=bd_handler.calculate)
    dpg.add_slider_int(tag='sldLHand', label="L. HAND", pos=(495, 160), width=100, default_value=100, callback=bd_handler.calculate)

    dpg.add_slider_int(tag='sldLLeg', label="L. LEG", pos=(495, 360), width=100, default_value=100, callback=bd_handler.calculate)
    dpg.add_slider_int(tag='sldLFeet', label="L. FEET", pos=(332, 490), width=100, default_value=100, callback=bd_handler.calculate)

    # other
    dpg.add_button(tag='btnHeal', label='HEAL', pos=(20, 20), callback=bd_handler.heal)

    dpg.add_checkbox(tag='chkArrow', label='Took an arrow in the knee', pos=(171, 520), callback=bd_handler.calculate)

    bd_handler.pgbHP = dpg.add_progress_bar(tag='pgbHP', label='HP', pos=(170, 550), width=310)
    dpg.add_text('HP', pos=(310, 550))

with dpg.window(tag='damageReport', label="DAMAGE REPORT", pos=(170, 570), width=310):
    bd_handler.txtReport = dpg.add_text('AAAAA', label='txtReport')


# debug position find window
#with dpg.window(label="posMaster", tag='posMaster'):
#    dpg.add_text("Hello world")
#    dpg.add_button(label="POS", callback=move_window)

dpg.set_primary_window("mainWindow", True)

dpg.show_viewport()
bd_handler.calculate('', '')
dpg.start_dearpygui()
dpg.destroy_context()
