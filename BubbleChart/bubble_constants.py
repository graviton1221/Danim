# for SPECIFIC_COLORS only
import pandas as pd

import numpy as np
from manimlib.constants import *


#-----------data settings 输入数据设置------------#
#************************************************#

DATA_DIR =  "Danim\\DATA"
file_name_list = ["X.csv","Y.csv","R.csv"]
X_file_name = "X.csv"
Y_file_name = "Y.csv"
R_file_name = "R.csv"
#Group_lables = "Group_lable.csv"
#************************************************#



#-----------axes settings坐标轴参数设置-----------#
#************************************************#

#whether to customize the axes range, 
#if not, the range is set by digest_data_and_set_the_axes()
#是否手动调节坐标轴范围
#可选择自动调节
CUSTOM_AXES_RANGE = True
# set the axes range yourself:
# 手动调节坐标轴范围
if CUSTOM_AXES_RANGE:
	XMIN = 0
	XMAX = 110
	YMIN = 0
	YMAX = 11

SHOW_AXIS_LABLES = True
X_AXIS_LABLE = "人均寿命"
Y_AXIS_LABLE = "生育率"
TEXT_COLOR = LIGHT_GREY
TEXT_SCALE_FACTOR = 0.8
X_LABLE_ADJUST_VECTOR = 0.8*LEFT + 0.5*UP #ADJUST THE X_AXIS_LABLE POSITION
Y_LABLE_ADJUST_VECTOR = 0.8*RIGHT + 0.5*DOWN

#pretty self-expainatory
SHOW_X_NUMBERS = True
SHOW_Y_NUMBERS = True
X_DECIMAL_PLACES = 0
Y_DECIMAL_PLACES = 0

# how big the axes numbers are, if shown
# 调节数轴数字大小
NUMBER_SCALE_FACTOR = 0.6

#axes origin point setting: default in the left bottom corner
#坐标原点设置: 默认在左下角 
#若要调节坐标位置 屏幕坐标原点为中间 屏幕总高8 宽约为14.22(8*1920/1080)
NEWORIGIN = np.array([-6.5,-3.5,0])

#whether customize the number shown on axes:
#if not, ticks will be evenly distributed on numberline
#是否手动调节坐标轴上显示的数字:
#如果不手动设置 则数字均匀分布在数轴上
CUSTOM_AXES_NUMBER = False

if CUSTOM_AXES_NUMBER:
	X_NUMBERS = range(-100,101,10)#list of numbers to show
	Y_NUMBERS = range(-100,101,10)
else:
	X_NUMBERS = []#list of numbers to show
	Y_NUMBERS = []
	NUM_OF_X_TICKS = 10
	NUM_OF_Y_TICKS = 10

#left most coordinates on screen, tip not included
#坐标轴最右侧的X坐标位置 不含箭头(不超过7.14, 否则超出屏幕)
RIGHT_MOST_X_ON_SCREEN = 7.
#top most coordinates on screen, tip not included
#坐标轴最上侧的X坐标位置 不含箭头(不超过4，否则超出屏幕)
TOP_MOST_Y_ON_SCREEN = 3.8

#axes color
AXIS_COLOR = LIGHT_GREY

#time_lable
TIME_LABLE_COLOR = PURPLE_E
TIME_LABLE_SCALE_FACTOR = 1.0
TIME_LABLE_POSITION = 6.0*RIGHT + 3.5*UP

#************************************************#


#-----------bubble settings 泡参数设置-----------#
#************************************************#

# default: 1.4 billion people is a 1.2unit area bubble
# 数据和泡泡面积的比值 用于调整泡泡面积大小的参数
# 默认设为2亿(人口)为1单位面积圆

#100亿为单位圆
R_per_circle_area =10000000000 #1000000000

#bubbles' opacity
#圆透明度
FILL_OPACITY = 0.7

#color generation group lables:
GROUP_LABLE_CSV_FILE = "Danim\\DATA\\Group_lable.csv"
COLOR_LABLE_DICT = {
	"AFRICA":RED,
	"ASIA":GREEN,
	"EUROPE":BLUE,
	"LATIN AMERICA AND THE CARIBBEAN":YELLOW,
	"OCEANIA":PURPLE_E
	}


'''
{"华北":YELLOW,"华南":ORANGE,"东北":WHITE,"华东":BLUE,"西南":RED,"华中":GREEN,"西北":TEAL_E}
'''

'''
{"TOP TIER":RED,"MID TIER":ORANGE,"BOTTOM TIER":YELLOW}
'''

'''{
	'仓位波动小':RED,
	'仓位波动适中':BLUE,
	'仓位波动大':YELLOW}
'''

'''
{
	"其他":RED,
	"宝盈基金":GREEN,
	"博时基金":PURPLE_E,
	"富国基金":BLUE,
	"华夏基金":YELLOW,
	"华安基金":DARK_BROWN,
	"汇添富基金":MAROON_E,
	"嘉实基金":PINK
	}


'''

'''
{
	"AFRICA":RED,
	"ASIA":GREEN,
	"EUROPE":BLUE,
	"LATIN AMERICA AND THE CARIBBEAN":YELLOW,
	"OCEANIA":PURPLE_E
	}
'''
GROUP_NAME = "Area_name"#group by which column name in file Group_lable.csv



THE_WHOLE_WORLD =["AFRICA","ASIA","EUROPE","LATIN AMERICA AND THE CARIBBEAN","OCEANIA"] #**
CH_THE_WHOLE_WORLD = ["非洲","亚洲","欧洲","美洲和加勒比","岛国"]
AREA_COLOR_MAP = [RED,GREEN,BLUE,YELLOW,PURPLE_E]
SOME_CONTRIES = []#["China","India","United States","United Kingdom","Russia"]



#color_lables
SHOWN_ENTITY_NAMES = COLOR_LABLE_DICT.keys() #default THE_WHOLE_WORLD
RECT_HIGHT = 0.2
RECT_WIDTH = 0.5
RECT_POSITION = 5.0*RIGHT + 3.0*UP
RECT_TEXT_SCALE_FACTOR = 0.4
SHOW_CN_NAMES = False # when True, the program only works if the Internet is connected
RECT_INTERVAL_FACTOR = 2 # default interval is (2-1) * the rectangle heights, must be greater than 1
NAME_TEXT_SCALE_FACTOR = 0.3
SINGLE_GROW_RUN_TIME = 0.8
SINGLE_TRANSFER_TIME = 0.8
NUM_OF_MAXIMUM_CIRCLES_IN_A_FRAME = 60 #used in get_creation for bubble chart
LAG_RATIO_FOR_CREATION = 0.3
#************************************************#


#-----------Animation settings 动画设置-----------#
#************************************************#
SHOW_CREATION = True
if SHOW_CREATION:
	CREATION_RUN_TIME = 2 #default 10s
else:
	CREATION_RUN_TIME = 0

SET_BY_TOTAL_TIME = True
TOTAL_TIME = 30 #default 30s
proportion_of_transformation = 0.3 #30% of the time set to transform
if SET_BY_TOTAL_TIME:
	BUBBLE_TRANSFROMATION_RUN_TIME = (TOTAL_TIME - CREATION_RUN_TIME)*proportion_of_transformation
	TIME_LABLE_TRANSFROMATION_RUN_TIME = BUBBLE_TRANSFROMATION_RUN_TIME/2
	WAIT_TIME = TOTAL_TIME - CREATION_RUN_TIME - BUBBLE_TRANSFROMATION_RUN_TIME
else:

	BUBBLE_TRANSFROMATION_RUN_TIME = 1
	TIME_LABLE_TRANSFROMATION_RUN_TIME = 0.5
	WAIT_TIME = 1

DISPLAY_SPECIFIC_ENTITIES = False

SOME_ENTITIES_TO_SHOW = SOME_CONTRIES #if DISPLAY_SPECIFIC_ENTITIES is True

COLOR_LABLE_INDEX_DICT = {}
for i,entity in enumerate(SHOWN_ENTITY_NAMES):
	COLOR_LABLE_INDEX_DICT[entity] = i

#************************************************#
