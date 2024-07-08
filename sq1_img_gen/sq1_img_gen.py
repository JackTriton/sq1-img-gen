import reflex as rx
from modules.img_genner import generate_image


class FormState(rx.State):
    form_data: dict = {}
    u_layer: bool = True
    e_layer: bool = True
    d_layer: bool = True
    img: str = ""
    bordercolor: str = "0, 0, 0"
    topcolor: str = "40, 40, 40"
    bottomcolor: str = "255, 255, 255"
    frontcolor: str = "255, 0, 0"
    backcolor: str = "255, 165, 0"
    leftcolor: str = "0, 73, 255"
    rightcolor: str = "0, 255, 0"
    shapecolor: str = "100, 100, 100"
    extensionfactor: str = "1.2"

    def handle_submit(self, form_data: dict):
        self.img = generate_image(form_data, 100)
  
    def change_U(self):
        self.u_layer = not self.u_layer

    def change_E(self):
        self.e_layer = not self.e_layer

    def change_D(self):
        self.d_layer = not self.d_layer


@rx.page(title="Seby's Square-1 Image Generator")
def index():
    return rx.container(
        rx.center(rx.heading("Seby's Square-1 Image Generator"), margin_bottom="10px"),

        rx.center(rx.link(rx.hstack("Need help?", rx.icon("circle-help")), href="https://github.com/Wo0fle/sq1-img-gen/blob/main/README.md", target="_blank"), margin_bottom="40px"),

        rx.hstack(
            rx.center(
                rx.vstack(
                    rx.heading("Input", margin_bottom="30px"),
                    rx.form.root(
                        rx.center(
                            rx.vstack(
                                rx.hstack(
                                    rx.text_area(
                                        placeholder="/ (3,0) / (-3,-3) / (0,3) /",
                                        name="text_input",
                                        variant="surface",
                                        size="2",
                                        rows="6",
                                    ),
                                    rx.radio(
                                        ["Case", "Algorithm", "State"],
                                        default_value="Case",
                                        name="input_type",
                                        spacing="3",
                                    ),
                                    rx.dialog.root(
                                        rx.dialog.trigger(rx.link(rx.icon("circle-help"), href="#")),
                                        rx.dialog.content(
                                            rx.vstack(
                                                rx.text(rx.text.strong("Case: "), "Your input will solve the Square-1 in the generated image."),
                                                rx.text(rx.text.strong("Algorithm: "), "Your input will be applied to a solved Square-1 to generate the image."),
                                                rx.text(rx.text.strong("State: "), "Your inputted ", rx.link("sq1optim", href="https://www.jaapsch.net/puzzles/square1.htm#progs", is_external=True), " state will be the Square-1's state in the generated image."),
                                                rx.link(rx.hstack("Need help?", rx.icon("circle-help")), href="https://github.com/Wo0fle/sq1-img-gen/blob/main/README.md", target="_blank"),
                                            ),
                                        ),
                                    ),
                                ),
                                rx.radio(
                                    ["Normal", "Orientation", "Shape"],
                                    default_value="Normal",
                                    name="scheme",
                                    direction="row",
                                    spacing="5",
                                    margin_bottom="10px"
                                ),
                                rx.hstack(
                                    rx.checkbox(
                                        name="include_U",
                                        on_change=FormState.change_U(),
                                        default_checked=True,
                                    ),
                                    rx.text("Include top layer")
                                ),
                                rx.hstack(
                                    rx.checkbox(
                                        name="include_E",
                                        on_change=FormState.change_E(),
                                        default_checked=True,
                                    ),
                                    rx.text("Include equator")
                                ),
                                rx.hstack(
                                    rx.checkbox(
                                        name="include_D",
                                        on_change=FormState.change_D(),
                                        default_checked=True,
                                    ),
                                    rx.text("Include bottom layer")
                                ),
                                rx.radio(
                                    ["Vertical", "Horizontal"],
                                    default_value="Vertical",
                                    name="img_orientation",
                                    direction="row",
                                    spacing="2",
                                    margin_top="10px"
                                ),
                                rx.cond(
                                    FormState.u_layer | FormState.e_layer | FormState.d_layer,
                                    rx.button(rx.icon("image"), "Generate", type="submit", margin_top="20px", margin_bottom="20px", size="3"),
                                    rx.button(rx.icon("image"), "Generate", margin_top="20px", margin_bottom="20px", size="3", disabled=True, variant="outline"),
                                ),
                                rx.vstack(
                                    rx.hstack(rx.text("Border color:"), rx.input(name="bordercolor", placeholder="Default: 0, 0, 0", value=FormState.bordercolor, on_change=FormState.set_bordercolor()), rx.box(width="15px", height="15px", border="1px solid gray", border_radius="50%", background_color=f"rgb({FormState.bordercolor})")),
                                    rx.html("<br>"),
                                    rx.hstack(rx.text("Top side color:"), rx.input(name="topcolor", placeholder="Default: 40, 40, 40", value=FormState.topcolor, on_change=FormState.set_topcolor()), rx.box(width="15px", height="15px", border="1px solid gray", border_radius="50%", background_color=f"rgb({FormState.topcolor})")),
                                    rx.hstack(rx.text("Bottom side color:"), rx.input(name="bottomcolor", placeholder="Default: 255, 255, 255", value=FormState.bottomcolor, on_change=FormState.set_bottomcolor()), rx.box(width="15px", height="15px", border="1px solid gray", border_radius="50%", background_color=f"rgb({FormState.bottomcolor})")),
                                    rx.hstack(rx.text("Front side color:"), rx.input(name="frontcolor", placeholder="Default: 255, 0, 0", value=FormState.frontcolor, on_change=FormState.set_frontcolor()), rx.box(width="15px", height="15px", border="1px solid gray", border_radius="50%", background_color=f"rgb({FormState.frontcolor})")),
                                    rx.hstack(rx.text("Back side color:"), rx.input(name="backcolor", placeholder="Default: 255, 165, 0", value=FormState.backcolor, on_change=FormState.set_backcolor()), rx.box(width="15px", height="15px", border="1px solid gray", border_radius="50%", background_color=f"rgb({FormState.backcolor})")),
                                    rx.hstack(rx.text("Left side color:"), rx.input(name="leftcolor", placeholder="Default: 0, 73, 255", value=FormState.leftcolor, on_change=FormState.set_leftcolor()), rx.box(width="15px", height="15px", border="1px solid gray", border_radius="50%", background_color=f"rgb({FormState.leftcolor})")),
                                    rx.hstack(rx.text("Right side color:"), rx.input(name="rightcolor", placeholder="Default: 0, 255, 0", value=FormState.rightcolor, on_change=FormState.set_rightcolor()), rx.box(width="15px", height="15px", border="1px solid gray", border_radius="50%", background_color=f"rgb({FormState.rightcolor})")),
                                    rx.html("<br>"),
                                    rx.hstack(rx.text("Shape color:"), rx.input(name="shapecolor", placeholder="Default: 100, 100, 100", value=FormState.shapecolor, on_change=FormState.set_shapecolor()), rx.box(width="15px", height="15px", border="1px solid gray", border_radius="50%", background_color=f"rgb({FormState.shapecolor})")),
                                    rx.html("<br>"),
                                    rx.hstack(
                                        rx.text("Extension factor: "),
                                        rx.input(name="extensionfactor", placeholder="Default: 1.2", value=FormState.extensionfactor, on_change=FormState.set_extensionfactor()),
                                        rx.dialog.root(
                                            rx.dialog.trigger(rx.link(rx.icon("circle-help"), href="#")),
                                            rx.dialog.content(
                                                rx.vstack(
                                                    rx.text(rx.text.strong("Extension factor"), " refers to how far the front/back/left/right sides of pieces extend from the top/bottom sides."),
                                                    rx.text(rx.text.strong("Values above 1"), " lead to the sides sticking out of the top/bottom."),
                                                    rx.text(rx.text.strong("Values below 1"), " lead to the sides sticking into the top/bottom."),
                                                    rx.text(rx.text.strong("A value of 1"), " leads to no visible side colors on the top/bottom layers."),
                                                    rx.link(rx.hstack("Need help?", rx.icon("circle-help")), href="https://github.com/Wo0fle/sq1-img-gen/blob/main/README.md", target="_blank"),
                                                ),
                                            ),
                                        ),
                                    ),
                                ),
                            ),
                        ),


                        on_submit=FormState.handle_submit,
                        reset_on_submit=False,
                    ),

                margin_bottom="30px",
                ),
            
            margin_top=0
            ),

            rx.vstack(
                rx.heading("Output", margin_top=0),
                rx.image(src=rx.get_upload_url(FormState.img)),

                margin_top=0
            ),
        
        margin_top=0,
        ),

        rx.logo(), rx.color_mode.button(position="bottom-right"),

        padding="20px",
    )


all_is_margin_auto = {
    "*": {
        "margin": "auto",
    },
}

app = rx.App(
    theme=rx.theme(appearance="dark"),
    accent_color="blue",
    style=all_is_margin_auto,
)
app.add_page(index)
