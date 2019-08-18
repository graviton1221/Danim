import os
import numpy as np
import pandas as pd
from os.path import join
from Danim.BubbleChart.bubble_constants import *
from manimlib.mobject.coordinate_systems import Axes
from manimlib.mobject.types.vectorized_mobject import VGroup
from manimlib.mobject.geometry import Circle
from Danim.Distribution import bubble_sort

#for online translation:
from urllib import request
from urllib import parse
import json


#-----------data digest数据输入变量X,Y,R,T处理 ---#
#************************************************#
def data_digest(
    DATADIR = DATA_DIR, 
    file_names = file_name_list,
    is_sorted = False,
    encoding = 'gbk', 
    display_specific_entities = DISPLAY_SPECIFIC_ENTITIES,
    entity_name_list = SOME_ENTITIES_TO_SHOW
    ): #default False

    # input data format convention(X,Y,R): is_sorted = True
    # X,Y,R data can be import from cvs file with format convention:
    # first column(but not the first row) includes all the entity names(not necessary)
    # first row(but not the first column) includes all the time interval names(not necessary)
    # from (2,2) TO (n,n) is all the data, left blank if none.

    # OR you can import data whatever way you want, 
    # just make sure the X,Y,R variables are np.ndarray
    
    
    assert(len(file_names) == 3)

    # if data is not sorted, csv file must have entity index(like names)
    # we have to use pandas to help us sort the valid data:
    if not is_sorted:
        data = []
        for file in file_names:#order is X,Y,R in file_names
            path = os.path.join(DATADIR,file)
            df = pd.read_csv(path,encoding = encoding ,index_col = 0)
            data.append(df)

        #find the entity names that are shown on all three dataframes 
        if not display_specific_entities:
            entity_index = list((set(data[0].index)&set(data[1].index)&set(data[2].index)))      
        else:
            entity_index = entity_name_list
        
        time_lables = list((set(data[0].columns)&set(data[1].columns)&set(data[2].columns)))#&
        bubble_sort(time_lables)
        
        for i in [0,1,2]:
            data[i] = pd.DataFrame(data[i], index = entity_index, columns = time_lables)

    return np.array(data[0]), np.array(data[1]), np.array(data[2]), entity_index, time_lables

#************************************************#

#-----------axes creation创建坐标轴方法-----------#
#************************************************#
def import_data_and_set_axes(

    #data inputs
    X,#the data that is projected to X axis, its shape should be (number of bubbles, number of time intervals)
    Y,#the data that is projected to Y axis, its shape should be (number of bubbles, number of time intervals)
    ):
    

    # This function is to deal with all sorts of data
    # that is about to be putted in the bubble charts,
    # The input X,Y must be np.ndarrays.

    #check whether the types and shapes of X,Y,R are correct
    assert(isinstance(X, np.ndarray) and isinstance(Y,np.ndarray))
    assert(X.shape == Y.shape and len(X.shape) == 2)

    #digest the range, if not custom range
    if not CUSTOM_AXES_RANGE:
        xmin = np.min(X)
        xmax = np.max(X)
        ymin = np.min(Y)
        ymax = np.max(Y)
    else:
        xmin = XMIN
        xmax = XMAX
        ymin = YMIN
        ymax = YMAX        

    if not CUSTOM_AXES_NUMBER:

        DISTANCE_BETWEEN_XAXIS_TICKS = np.divide(xmax - xmin,NUM_OF_X_TICKS + 1)
        DISTANCE_BETWEEN_YAXIS_TICKS = np.divide(ymax - ymin,NUM_OF_Y_TICKS + 1)

        x_axis_config = {
            "tick_frequency": DISTANCE_BETWEEN_XAXIS_TICKS,
            "leftmost_tick": xmin,            
            "numbers_with_elongated_ticks":[ymin],
            "decimal_number_config": {
                "num_decimal_places": X_DECIMAL_PLACES,
                }   
            }
        y_axis_config = {
        	"label_direction": LEFT,
            "tick_frequency": DISTANCE_BETWEEN_YAXIS_TICKS,
            "leftmost_tick": ymin,
            "numbers_with_elongated_ticks":[ymin],
            "decimal_number_config": {
                "num_decimal_places": Y_DECIMAL_PLACES,
                }    
            }            
    else:
        x_axis_config = {"include_ticks":False}
        y_axis_config = {"include_ticks":False,"label_direction": LEFT}
        #add numbers and ticks manully

    #create the axis config:
    AXES_CONFIG = {        
        #axis information
        "x_min": xmin,
        "x_max": xmax,
        "y_min": ymin,
        "y_max": ymax,

        # MORE axis config at mobject.number_line.py
        "x_axis_config":x_axis_config,
        "y_axis_config":y_axis_config,
        "number_line_config": {
            "color": AXIS_COLOR,
            "include_tip": True,
            "exclude_zero_from_default_numbers": True,
            "number_scale_val":NUMBER_SCALE_FACTOR}
        }

    #create the axes mobject
    axes = Axes(
            x_min = AXES_CONFIG["x_min"],
            x_max = AXES_CONFIG["x_max"],
            y_min = AXES_CONFIG["y_min"],
            y_max = AXES_CONFIG["y_max"],
            x_axis_config = AXES_CONFIG["x_axis_config"],
            y_axis_config = AXES_CONFIG["y_axis_config"],
            number_line_config = AXES_CONFIG["number_line_config"],
            )

    #adjust the axes position to fit the screen:
    x_scale_factor = np.divide(RIGHT_MOST_X_ON_SCREEN - NEWORIGIN[0],xmax - xmin)
    y_scale_factor = np.divide(TOP_MOST_Y_ON_SCREEN - NEWORIGIN[1],ymax - ymin)
    axes.x_axis.shift(xmin*LEFT)
    axes.y_axis.shift(ymin*DOWN)
    axes.x_axis.stretch_about_point(x_scale_factor, 0, ORIGIN)
    axes.y_axis.stretch_about_point(y_scale_factor, 1, ORIGIN)
    axes.shift(NEWORIGIN)

    # create customized numbers and ticks to axes
    if CUSTOM_AXES_NUMBER:
        axes.x_axis.tick_marks = VGroup()
        axes.y_axis.tick_marks = VGroup()
        for number in X_NUMBERS:
            axes.x_axis.tick_marks.add(axes.x_axis.get_tick(number))
            axes.x_axis.add_numbers(number)
        for number in Y_NUMBERS:
            axes.y_axis.tick_marks.add(axes.y_axis.get_tick(number))
            axes.y_axis.add_numbers(number)
        axes.x_axis.add(axes.x_axis.tick_marks)
        axes.y_axis.add(axes.y_axis.tick_marks)
    
    else:
    	if SHOW_X_NUMBERS:
    		interates = np.linspace(xmin,xmax,NUM_OF_X_TICKS + 1, endpoint = False)
    		np.delete(interates,0)
    		for number in interates:
    			axes.x_axis.add_numbers(number)
    	if SHOW_Y_NUMBERS:
    		interates = np.linspace(ymin,ymax,NUM_OF_Y_TICKS + 1, endpoint = False)
    		np.delete(interates,0)
    		for number in interates:
    			axes.y_axis.add_numbers(number)
	
    return AXES_CONFIG, axes

def transform_from_data_to_screencoordinates(X,Y,R,axes):
    #transform X,Y,R data into screen coordinates:

    #dimension check
    assert(X.shape == Y.shape and Y.shape == R.shape)
    assert(isinstance(X,np.ndarray) and isinstance(Y,np.ndarray) and isinstance(R,np.ndarray))


    #X&Y transformation:    
    x_alpha = np.divide(RIGHT_MOST_X_ON_SCREEN - NEWORIGIN[0],axes.x_axis.x_max - axes.x_axis.x_min)
    y_alpha = np.divide(TOP_MOST_Y_ON_SCREEN  - NEWORIGIN[1],axes.y_axis.x_max - axes.y_axis.x_min)

    X = (X - axes.x_axis.x_min)*x_alpha + NEWORIGIN[0]
    Y = (Y - axes.y_axis.x_min)*y_alpha + NEWORIGIN[1]

    #TODO: add third dimension?
    Z = np.zeros(X.shape)

    coordinates = np.stack([X,Y,Z],axis = 2)

    #R transformation: Rdata represents the bubble radius
    #but the R represents bubble area, not the radius
    Rdata = np.sqrt(np.divide(2*np.divide(R,R_per_circle_area),np.pi))

    return coordinates,Rdata

def set_up_the_bubbles(coordinates_at_a_time, Rdata_at_a_time, axes, color_mat):

    # the argument coordinates_at_a_time and Rdata_at_a_time is 
    # just one column in coordinates and Rdata
    # specifically coordinates_at_a_time = coordinates[:,0]
    # Rdata_at_a_time = Rdata[:,0]

    #dimension check
    assert(coordinates_at_a_time.shape[0] == Rdata_at_a_time.shape[0] and len(color_mat))
    assert(len(coordinates_at_a_time.shape) == 2)
    assert(isinstance(color_mat,list))
    

    bubbles = VGroup()
    for i,bubbledata in enumerate(zip(coordinates_at_a_time,Rdata_at_a_time)):
        bubbles.add(
            Circle(
                radius = bubbledata[1], 
                color = color_mat[i], 
                fill_opacity = FILL_OPACITY).shift(bubbledata[0])
            )

    return bubbles

#-----------other useful tools 其他工具-----------#
#************************************************#

def online_translation(English_string):
     # 对应上图的Request URL
    request_url = "http://fanyi.youdao.com/translate?smartresult=dict&smartresult=rule"
    # 创建Form Data字典，存储上图中的Form Data
    Form_Data = {}
    Form_Data['i'] = English_string
    Form_Data['from'] = 'AUTO'
    Form_Data['to'] = 'AUTO'
    Form_Data['smartresult'] = 'dict'
    Form_Data['client'] = 'fanyideskweb'
    Form_Data['doctype'] = 'json'
    Form_Data['version'] = '2.1'
    Form_Data['keyfrom'] = 'fanyi.web'
    Form_Data['action'] = 'FY_BY_REALTIME'
    Form_Data['typoResult'] = 'false'
    # 使用urlencode方法转换标准格式
    data = parse.urlencode(Form_Data).encode('utf-8')
    # 传递Request对象和转换完格式的数据
    response = request.urlopen(request_url, data)
    # 读取信息并解码
    html = response.read().decode('utf-8')
    # 使用json
    translate_results = json.loads(html)
    # 找到翻译结果
    translate_result = translate_results["translateResult"][0][0]['tgt']
    return translate_result
