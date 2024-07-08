import reflex as rx
import drawsvg as draw
import math
import time
from virtual_sq1 import Square1
from modules.color_scheme import get_color


def generate_image(form_data, cube_side_length):
    """
    Generates the Square-1 image with a cube of
    side length `cube_side_length` (in pixels) using
    `form_data` and saves to `path_to_save_to`.
    """

    squan = Square1()

    if form_data["input_type"] == "Case":
        squan.apply_alg(form_data["text_input"], True)
    elif form_data["input_type"] == "Algorithm":
        squan.apply_alg(form_data["text_input"])
    else:
        squan.apply_state(form_data["text_input"])

    border_color = form_data["bordercolor"]

    top_color = form_data["topcolor"]
    bottom_color = form_data["bottomcolor"]
    front_color = form_data["frontcolor"]
    back_color = form_data["backcolor"]
    left_color = form_data["leftcolor"]
    right_color = form_data["rightcolor"]

    shape_color = form_data["shapecolor"]

    img_width = cube_side_length * 2
    img_height = img_width * 2.15

    extension_factor = float(form_data["extensionfactor"])
    border_thickness = int((1/130)*img_width)

    color_list = [front_color, left_color, back_color, right_color]

    half_edge_length = (cube_side_length/2)*(math.tan(15*(math.pi/180)))
    edge_height = (cube_side_length/2)
    corner_side_length = edge_height - half_edge_length

    edge_vector = [-half_edge_length, edge_height]
    half_diag_vector = [-cube_side_length/2, cube_side_length/2]

    # init
    if form_data["img_orientation"] == "Vertical":
        d = draw.Drawing(img_width, img_height, origin='center')
        u_coord = (0, -1.1*cube_side_length)
        e_coord = (0, 0)
        d_coord = (0, 1.1*cube_side_length)
    else:
        d = draw.Drawing(img_height, 1.2*img_width, origin='center')
        u_coord = (-cube_side_length, 0)
        e_coord = (0, (cube_side_length/2)+corner_side_length)
        d_coord = (cube_side_length, 0)

    # draw top
    rotate_by = 0

    if form_data.get("include_U") == "on":
        translate = f"translate{u_coord}"

        if extension_factor >= 1 or extension_factor <= 1:
            d.append(draw.Line(edge_vector[0]*(extension_factor*1.2), edge_vector[1]*(extension_factor*1.2),
                                edge_vector[0]*-(extension_factor*1.2), edge_vector[1]*-(extension_factor*1.2),
                                stroke=f"rgb({border_color})", stroke_width=border_thickness,
                                transform=f"{translate}"))
        else:
            d.append(draw.Line(edge_vector[0]*1.2, edge_vector[1]*1.2,
                                edge_vector[0]*-1.2, edge_vector[1]*-1.2,
                                stroke=f"rgb({border_color})", stroke_width=border_thickness,
                                transform=f"{translate}"))
        
        for piece in squan.top.__str__():
            rotation= f"rotate({rotate_by})"

            if piece in "ABCDEFGH":
                if form_data["scheme"] != "Shape":
                    if piece in "ABCD":
                        current_color = top_color
                    else:
                        current_color = bottom_color
                else:
                    current_color = shape_color

                d.append(draw.Lines(0, 0,
                                    edge_vector[0], edge_vector[1],
                                    half_diag_vector[0], half_diag_vector[1],
                                    half_diag_vector[0], -edge_vector[0],
                                    close=True,
                                    fill=f"rgb({current_color})",
                                    stroke=f"rgb({border_color})", stroke_width=border_thickness,
                                    transform=f"{translate} {rotation}"))

                if form_data["scheme"] == "Normal":
                    d.append(draw.Lines(
                                    edge_vector[0], edge_vector[1],
                                    edge_vector[0]*extension_factor, edge_vector[1]*extension_factor,
                                    half_diag_vector[0]*extension_factor, half_diag_vector[1]*extension_factor,
                                    half_diag_vector[0], half_diag_vector[1],
                                    close=True,
                                    fill=f"rgb({get_color(color_list, piece)})",
                                    stroke=f"rgb({border_color})", stroke_width=border_thickness,
                                    transform=f"{translate} {rotation}"))
                    d.append(draw.Lines(
                                    half_diag_vector[0], half_diag_vector[1],
                                    half_diag_vector[0]*extension_factor, half_diag_vector[1]*extension_factor,
                                    half_diag_vector[0]*extension_factor, -edge_vector[0]*extension_factor,
                                    half_diag_vector[0], -edge_vector[0],
                                    close=True,
                                    fill=f"rgb({get_color(color_list, piece, 1)})",
                                    stroke=f"rgb({border_color})", stroke_width=border_thickness,
                                    transform=f"{translate} {rotation}"))

                rotate_by += 60
            else:
                if form_data["scheme"] != "Shape":
                    if piece in "1234":
                        current_color = top_color
                    else:
                        current_color = bottom_color
                else:
                    current_color = shape_color

                d.append(draw.Lines(0, 0,
                                    edge_vector[0], edge_vector[1],
                                    edge_vector[0]-(2*half_edge_length*math.cos(30*math.pi/180)), edge_vector[1]-(2*half_edge_length*math.sin(30*math.pi/180)),
                                    close=True,
                                    fill=f"rgb({current_color})",
                                    stroke=f"rgb({border_color})", stroke_width=border_thickness,
                                    transform=f"{translate} {rotation}"))

                if form_data["scheme"] == "Normal":
                    d.append(draw.Lines(
                                    edge_vector[0], edge_vector[1],
                                    edge_vector[0]*extension_factor, edge_vector[1]*extension_factor,
                                    extension_factor*(edge_vector[0]-(2*half_edge_length*math.cos(30*math.pi/180))), extension_factor*(edge_vector[1]-(2*half_edge_length*math.sin(30*math.pi/180))),
                                    edge_vector[0]-(2*half_edge_length*math.cos(30*math.pi/180)), edge_vector[1]-(2*half_edge_length*math.sin(30*math.pi/180)),
                                    close=True,
                                    fill=f"rgb({get_color(color_list, piece)})",
                                    stroke=f"rgb({border_color})", stroke_width=border_thickness,
                                    transform=f"{translate} {rotation}"))

                rotate_by += 30

    # draw equator
    if form_data.get("include_E") == "on":
        translate = f"translate{e_coord}"

        if form_data["scheme"] != "Normal":
            left_eq_color = shape_color
            right_eq_color = shape_color
        else:
            left_eq_color = front_color
            right_eq_color = front_color

            if squan.equator_flipped:
                right_eq_color = back_color

        d.append(draw.Rectangle(-cube_side_length/2, -half_edge_length,
                                corner_side_length, (2*half_edge_length),
                                fill=f"rgb({left_eq_color})",
                                stroke=f"rgb({border_color})", stroke_width=border_thickness,
                                transform=f"{translate}"))

        if not squan.equator_flipped:
            d.append(draw.Rectangle(-half_edge_length, -half_edge_length,
                                corner_side_length+(2*half_edge_length), (2*half_edge_length),
                                fill=f"rgb({right_eq_color})",
                                stroke=f"rgb({border_color})", stroke_width=border_thickness,
                                transform=f"{translate}"))
        else:
            d.append(draw.Rectangle(-half_edge_length, -half_edge_length,
                                corner_side_length, (2*half_edge_length),
                                fill=f"rgb({right_eq_color})",
                                stroke=f"rgb({border_color})", stroke_width=border_thickness,
                                transform=f"{translate}"))

    # draw bottom
    rotate_by = 150

    if form_data.get("include_D") == "on":
        translate = f"translate{d_coord}"

        if extension_factor >= 1 or extension_factor <= 1:
            d.append(draw.Line(edge_vector[0]*(extension_factor*1.2), edge_vector[1]*(extension_factor*1.2),
                                edge_vector[0]*-(extension_factor*1.2), edge_vector[1]*-(extension_factor*1.2),
                                stroke=f"rgb({border_color})", stroke_width=border_thickness,
                                transform=f"{translate} rotate(-30)"))
        else:
            d.append(draw.Line(edge_vector[0]*1.2, edge_vector[1]*1.2,
                                edge_vector[0]*-1.2, edge_vector[1]*-1.2,
                                stroke=f"rgb({border_color})", stroke_width=border_thickness,
                                transform=f"{translate} rotate(-30)"))

        for piece in squan.bottom.__str__():
            rotation= f"rotate({rotate_by})"

            if piece in "ABCDEFGH":
                if form_data["scheme"] != "Shape":
                    if piece in "ABCD":
                        current_color = top_color
                    else:
                        current_color = bottom_color
                else:
                    current_color = shape_color

                d.append(draw.Lines(0, 0,
                                    edge_vector[0], edge_vector[1],
                                    half_diag_vector[0], half_diag_vector[1],
                                    half_diag_vector[0], -edge_vector[0],
                                    close=True,
                                    fill=f"rgb({current_color})",
                                    stroke=f"rgb({border_color})", stroke_width=border_thickness,
                                    transform=f"{translate} {rotation}"))

                if form_data["scheme"] == "Normal":
                    d.append(draw.Lines(
                                    edge_vector[0], edge_vector[1],
                                    edge_vector[0]*extension_factor, edge_vector[1]*extension_factor,
                                    half_diag_vector[0]*extension_factor, half_diag_vector[1]*extension_factor,
                                    half_diag_vector[0], half_diag_vector[1],
                                    close=True,
                                    fill=f"rgb({get_color(color_list, piece)})",
                                    stroke=f"rgb({border_color})", stroke_width=border_thickness,
                                    transform=f"{translate} {rotation}"))
                    d.append(draw.Lines(
                                    half_diag_vector[0], half_diag_vector[1],
                                    half_diag_vector[0]*extension_factor, half_diag_vector[1]*extension_factor,
                                    half_diag_vector[0]*extension_factor, -edge_vector[0]*extension_factor,
                                    half_diag_vector[0], -edge_vector[0],
                                    close=True,
                                    fill=f"rgb({get_color(color_list, piece, 1)})",
                                    stroke=f"rgb({border_color})", stroke_width=border_thickness,
                                    transform=f"{translate} {rotation}"))

                rotate_by += 60
            else:
                if form_data["scheme"] != "Shape":
                    if piece in "1234":
                        current_color = top_color
                    else:
                        current_color = bottom_color
                else:
                    current_color = shape_color

                d.append(draw.Lines(0, 0,
                                    edge_vector[0], edge_vector[1],
                                    edge_vector[0]-(2*half_edge_length*math.cos(30*math.pi/180)), edge_vector[1]-(2*half_edge_length*math.sin(30*math.pi/180)),
                                    close=True,
                                    fill=f"rgb({current_color})",
                                    stroke=f"rgb({border_color})", stroke_width=border_thickness,
                                    transform=f"{translate} {rotation}"))

                if form_data["scheme"] == "Normal":
                    d.append(draw.Lines(
                                    edge_vector[0], edge_vector[1],
                                    edge_vector[0]*extension_factor, edge_vector[1]*extension_factor,
                                    extension_factor*(edge_vector[0]-(2*half_edge_length*math.cos(30*math.pi/180))), extension_factor*(edge_vector[1]-(2*half_edge_length*math.sin(30*math.pi/180))),
                                    edge_vector[0]-(2*half_edge_length*math.cos(30*math.pi/180)), edge_vector[1]-(2*half_edge_length*math.sin(30*math.pi/180)),
                                    close=True,
                                    fill=f"rgb({get_color(color_list, piece)})",
                                    stroke=f"rgb({border_color})", stroke_width=border_thickness,
                                    transform=f"{translate} {rotation}"))

                rotate_by += 30

    filename = f"{squan.top}{squan.bottom}_{int(time.time())}.svg"

    d.save_svg(f"{rx.get_upload_dir()}/{filename}")

    return filename
