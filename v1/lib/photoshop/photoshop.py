import os
from osrparse import Replay
import photoshop as photoshop_package
import photoshop.api as photoshop_api
from lib import logger
import lib.osu

from lib.paths import OUTPUT_DIRECTORY, PHOTOSHOP_TEMPLATES_PATH

def change_text(photoshop_session:photoshop_package.Session, target_layer:str, new_text:str):
    layer = photoshop_session.app.activeDocument.artLayers[target_layer]
    layer.TextItem.contents = f"{new_text}"

def change_image(photoshop_session:photoshop_package.Session, layer:str, image_path:str):
    application = photoshop_session.app

    document = application.activeDocument
    document.activeLayer = document.artLayers[layer]
    
    descriptor = photoshop_session.ActionDescriptor
    descriptor.putPath(application.charIDToTypeID("null"), image_path)

    logger.info(f"Layer '{layer}' to image '{image_path}' change being executed")
    try:    
        application.executeAction(application.stringIDToTypeID("placedLayerReplaceContents"), descriptor)
    except:
        logger.error(f"Layer '{layer}' to image '{image_path}' change wasn't be able to be executed")
    else:
        logger.debug(f"Layer '{layer}' to image '{image_path}' change was excecuted sucessfully")

def resize_fit_image(photoshop_session:photoshop_package.Session, layer, max_size_x, max_size_y):
    logger.debug(f"Resizing layer {layer} to max_x {max_size_x} and max_y {max_size_y}")
    document = photoshop_session.app.activeDocument
    layer_bounds = photoshop_session.app.activeDocument.artLayers[layer].bounds
    
    # Size of X Axis Of Layer
    size_x = layer_bounds[2] - layer_bounds[0]
    rate_x = max_size_x / size_x
    
    # Size of Y Axis Of Layer
    size_y = layer_bounds[3] - layer_bounds[1]
    rate_y = max_size_y / size_y
    
    # Get which side is smaller, to fill the resolution without extra size
    percentage = (max_size_x / size_x * 100) if rate_x > rate_y else (max_size_y / size_y * 100)
    
    logger.info(f"Photoshop layer '{layer}' resizing being resized")
    try:
        document.artLayers[layer].Resize(percentage, percentage)
    except:
        logger.error(f"It wasn't possible to resize layer {layer} with max_x {max_size_x} and max_y {max_size_y}. Check if the {layer} exists at the project")
    else:
        logger.debug(f"Photoshop layer '{layer}' resizing was sucessful")

def export_image_jpeg(photoshop_session:photoshop_package.Session, quality_percentage:int, output_path:str):
    quality = round((14 * quality_percentage) / 100)
    
    save_options = photoshop_api.JPEGSaveOptions(quality=quality)
    save_options.formatOptions = photoshop_api.FormatOptionsType.StandardBaseline
    
    photoshop_session.app.activeDocument.saveAs(output_path, save_options, True)    

def close_photoshop():
    os.system("taskkill /F /IM photoshop.exe")

def funreplays_edit(output_name:str, player_name:str, replay_info:Replay, pp:float, star_rating:float, map_difficulty:str, map_name:str, leaderboard_position:str, beatmap_background_path:str, user_avatar_path:str):
    PROJECT_PATH = os.path.join(PHOTOSHOP_TEMPLATES_PATH, "4funreplays.psd")
    
    mods = (str(replay_info.mod_combination).replace('Mod.', '').replace('|', '').replace("NoMod", "").replace('NoFail', 'NF').replace('NightcoreDoubleTime', 'DT').replace('Nightcore', 'NC').replace('DoubleTime', 'DT').replace('HardRock', 'HR').replace('HalfTime', 'HT').replace('Easy', 'EZ').replace('Flashlight', "FL").replace('Hidden', "HD").replace("DTHD", "HDDT").replace("HRHD", "HDHR"))

    accuracy = lib.osu.calculate_accuracy(replay_info.number_300s, replay_info.number_100s, replay_info.number_50s, replay_info.misses)
    
    max_string_len = 50
    photoshop_edits = {
        "gdiffmapa" : f"[{map_difficulty}]" if len(map_difficulty) < max_string_len else f"[{map_difficulty[:max_string_len - 3]}...]",
        "gsr" : f"{star_rating}*",
        "gmods" : f"{f'+{mods}' if len(mods) > 0 else ''}",
        "gpp" : f"{round(pp)}pp",
        "gacc" : f"{accuracy}%",
        "gjogador" : player_name,
        "gnomemapa" : map_name if len(map_name) < max_string_len else f"{map_name[:max_string_len - 3]}...",
        "comentario" : f"#{leaderboard_position} GLOBAL" if leaderboard_position > 0 else ""
    }
    print(PROJECT_PATH)
    
    with photoshop_package.Session(PROJECT_PATH, action="open") as photoshop_session:
        application = photoshop_session.app
        document = application.activeDocument
        
        for photoshop_variable, corresponding_value in photoshop_edits.items():
            current_layer = document.artLayers[photoshop_variable]
            current_layer.TextItem.contents = f"{corresponding_value}"

        ## DOCUMENTAÇÃO
        ## https://photoshop-python-api.readthedocs.io/en/master/
        ## https://theiviaxx.github.io/photoshop-docs/Photoshop/Layer.html
        ## https://gist.github.com/laryn/0a1f6bf0dab5b713395a835f9bfa805c
        ## https://helperbyte.com/questions/57330/how-to-change-image-size-in-photoshop-script
        ## FIM
        
        for layer, text in photoshop_edits.items():
            change_text(photoshop_session, layer, text)
            
        change_image(photoshop_session, "profile_picture", user_avatar_path)
        resize_fit_image(photoshop_session, "profile_picture", 419, 419)
        
        change_image(photoshop_session, "background", beatmap_background_path)
        resize_fit_image(photoshop_session, "background", 1920, 1080)

        export_image_jpeg(photoshop_session, 75, os.path.join(OUTPUT_DIRECTORY, f"{output_name}"))
        
        close_photoshop()