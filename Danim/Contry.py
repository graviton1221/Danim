from big_ol_pile_of_manim_imports import *
import csv
import math
from Danim.Distribution import *

#---------- for online translation:
from urllib import request
from urllib import parse
import json
#-------------------------------



#---------------------------全局变量Constants:
DATADIR = "D:\\Anaconda3\\envs\\MAINM\\Lib\\manim\\Danim\\DATA"#存储数据的路径
population_data_file = "population_total.csv"
life_expectancy_data_file = "life_expectancy_years.csv"
children_per_woman_data_file = "children_per_woman_total_fertility.csv"
contry_and_area_file = "contry_and_area.csv"

#坐标轴设置axes settings FOR demo1(contry circles)
'''
population_per_circle_area = 1/1.4*1.2 # default: 1.4 billion people is a 1.2unit area circle

xmin = 0
xmax = 100
ymin = 0
ymax = 100
proportion_to_left = 0.9 #default x axis move to 10% empty space left, note its the proportion to the origin
proportion_to_bottom = 0.8
x_scale_factor = (proportion_to_left+1)*FRAME_X_RADIUS/(xmax-xmin)*0.96 # 0.96 is arrow buff
y_scale_factor = (proportion_to_bottom+1)*FRAME_Y_RADIUS/(ymax-ymin)*0.96
NEWORIGIN = [-FRAME_X_RADIUS*proportion_to_left,-FRAME_Y_RADIUS*proportion_to_bottom,0]
'''

#Verson2
#坐标轴设置settings for Danim\video1\4MoreComparison.py
population_per_circle_area = 1/1.4*1.2 # default: 1.4 billion people is a 1.2unit area circle
xmin = 0
xmax = 10
ymin = 0
ymax = 100
proportion_to_left = 0.9 #default x axis move to 10% empty space left, note its the proportion to the origin
proportion_to_bottom = 0.8
x_scale_factor = (proportion_to_left+1)*FRAME_X_RADIUS/(xmax-xmin)*0.96 # 0.96 is arrow buff
y_scale_factor = (proportion_to_bottom+1)*FRAME_Y_RADIUS/(ymax-ymin)*0.96
NEWORIGIN = [-FRAME_X_RADIUS*proportion_to_left,-FRAME_Y_RADIUS*proportion_to_bottom,0]


#坐标轴设置axes settings FOR demo2(contry income distribution)
population_per_distribution_area = 1.5/1.4 # 1.4billion people is area of 5 unit area
DEFAULT_CONFIDENCE_INTERVAL = 0.995
DEFAULT_DISTRIBUTION_OPACITY = 0.3
dis_xmin = -3
dis_xmax = 3
dis_ymin = -1
dis_ymax = 6.8
dis_proportion_to_left = 0.1 #default x axis move to 10% empty space left, note its the proportion to the origin
dis_proportion_to_bottom = 0.8
#x_scale_factor = (dis_proportion_to_left+1)*FRAME_X_RADIUS/(dis_xmax-dis_xmin)*0.96 # 0.96 is arrow buff
dis_x_axis_stretch_factor = 3
dis_y_scale_factor = (dis_proportion_to_bottom+1)*FRAME_Y_RADIUS/(dis_ymax-dis_ymin)*0.96
dis_NEWORIGIN = [-FRAME_X_RADIUS*dis_proportion_to_left,-FRAME_Y_RADIUS*dis_proportion_to_bottom,0]

#data_variable---------------------------------------------

THE_WHOLE_WORLD =["AFRICA","ASIA","EUROPE","LATIN AMERICA AND THE CARIBBEAN","OCEANIA"]
CH_THE_WHOLE_WORLD = ["非洲","亚洲","欧洲","美洲和加勒比","岛国"]
AREA_COLOR_MAP = [GREEN,RED,YELLOW,BLUE,PURPLE_E]
AREA_COLOR_MAP_DIC = {"AFRICA":GREEN,"ASIA":RED,"EUROPE":YELLOW,"LATIN AMERICA AND THE CARIBBEAN":BLUE,"OCEANIA":PURPLE_E}
LABLE_POINT = np.array([-5,-3,0]) #place to put the contry_name_lable and when the pointer

#log scale axis settings:---------------------------
LOG_BASE = 10.
LOG_FACTOR = 5. # the logscale X axis, each tick represents Y = LOG_FACTOR * LOG_BASE ** X
num_of_days_per_year = 365


# Currency:
EXCHANGE_RATE_FOR_RMB_TO_INTERNATIONAL_DOLLAR = 3.6 #3.48 in 2010-2015 

#------------------------全局方法:

def coordinate_origin_to_new(points):
#将二维数据映射至屏幕特定坐标轴的坐标点
    if not len(points) == 3:
        raise Exception("points must be a 3 lenthes list or nparray")
    else:
        newpoints = [
            (points[0]-xmin)*x_scale_factor+NEWORIGIN[0],
            (points[1]-ymin)*y_scale_factor+NEWORIGIN[1],
            0
            ]
    return newpoints

def coordinate_new_to_origin(points):
#将屏幕特定坐标轴的坐标点映射至二维数据    
    if not len(points) == 3:
        raise Exception("points must be a 3 lenthes list or nparray")
    else:
        newpoints = [
            (points[0]-NEWORIGIN[0])/x_scale_factor + xmin,
            (points[1]-NEWORIGIN[1])/y_scale_factor +ymin,
            0
            ]
    return newpoints

def get_circle_critical_point(circle,alpha = PI*5/4,buff = 0.1):
    #alpha is the angle of direction, default RIGHT DOWN direction
    if isinstance(circle,Circle):
        return (circle.get_center()+ (circle.get_width()/2 + buff)*np.array([np.cos(alpha),np.sin(alpha),0]))
    else:
        raise Exception("the first argument must be a type of mobject Circle")

#AXES set up
def set_up_the_appropriate_axes(axes_config):
    #TODO: set up axes more efficient, need to analyze data and set the appropriate axes config first
    pass


def online_translation(English_string):
    if English_string == "Georgia":
        translate_result =  "格鲁吉亚"
    elif English_string == "Timor-Leste":
        translate_result =  "东帝汶"
    elif English_string == "Turkey":
        translate_result =  "土耳其"
    elif English_string == "Uganda":
        translate_result =  "乌干达"
    elif English_string == "United Kingdom":
        translate_result =  "英国"
    elif English_string == "Zambia":
        translate_result =  "赞比亚"
    elif English_string == "Congo, Dem. Rep.":
        translate_result =  "刚果金"        
    elif English_string == "Congo, Rep.":
        translate_result =  "刚果布"
    elif English_string == "Madagascar":
        translate_result =  "马达加斯加"
    elif English_string == "Sao Tome and Principe":
        translate_result =  "圣多美和普林西比"
    elif English_string == "Togo":
        translate_result =  "多哥"
    elif English_string == "Bosnia and Herzegovina":
        translate_result =  "波黑"
    elif English_string == "Holy See":
        translate_result =  "梵蒂冈"    
    elif English_string == "San Marino":
        translate_result =  "圣马力诺"  
    elif English_string == "Antigua and Barbuda":
        translate_result =  "安提瓜和巴布达" 
    elif English_string == "Bahamas":
        translate_result =  "巴哈马" 
    elif English_string == "Bolivia":
        translate_result =  "玻利维亚" 
    elif English_string == "Costa Rica":
        translate_result =  "哥斯达黎加" 
    elif English_string == "El Salvador":
        translate_result =  "萨尔瓦多" 
    elif English_string == "Trinidad and Tobago":
        translate_result =  "特立尼达和多巴哥" 
    elif English_string == "Macedonia, FYR":
        translate_result =  "马其顿共和国" 
    elif English_string == "Micronesia, Fed. Sts.":
        translate_result =  "密克罗尼西亚联邦" 
    elif English_string == "Palau":
        translate_result =  "帕劳共和国" 
    elif English_string == "Tonga":
        translate_result =  "汤加" 
    elif English_string == "Tuvalu":
        translate_result =  "图瓦卢" 


    else:

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

#------------------------------------

'''
data_file_name choose from:
population data = "population_total.csv"
life expect data = "life_expectancy_years.csv"
children per woman data = "children_per_woman_total_fertility.csv"


attributes:

name: string

population_total: number
population_data_unit: number

shape: mobject (default circle)

contry_name: TextMobject
population_lable: TextMobject
population_lable_unit: TextMobject
data_coordinate_lable: TextMobject
data_x_lable: number mobject
data_y_lable: number mobject
MORE....
''' 

class Contry():

    def __init__(self, name = "China", shape = "Circle", show_CN_name = False):
        if isinstance(name,str):
            self.name = name # set the contry name, default China
            self.show_contry_name_lable = False
            self.show_CN_name = show_CN_name
        else:
            raise Exception("input name type must be string")

        if show_CN_name:
            #NEED to connect to Internet to run this function
            self.CN_name = online_translation(name)
            

        if shape == "Circle":
            self.circleconfig = {
                "show_contry_name": False,#a config used in circle shape
                "show_population_lable": False,#a config used in circle shape
                "numbers_scale_factor": 0.5, # a config used in circle shape numbers}
                "position_of_the_lable": RIGHT + DOWN,
                "distance_between_lable_and_unit":0.1*RIGHT,
                }

        if shape == "Distribution":
            self.distributionconfig = {
                "log_normal": True,
                "show_population_lable": False,#a config used in distribution shape
                "numbers_scale_factor": 0.5, # a config used in distribution shape numbers}
                "position_of_the_lable": RIGHT + DOWN,
                "distance_between_lable_and_unit":0.1*RIGHT,
            }


#Data Exraction:

    def exract_data_fromcsv(self, start_years = 1800, end_years = 2018, data_file_name ="population_total.csv",min_year = 1800):
        #exact contrydata from file csvfile with format: 1st row as (years)&1st col as (contry names)& others as (contry data)
        #min_year :the initial year in the table 'population_total.csv'
        """
        if you are using my dataset, the filename convention is: 
            population data in "population_total.csv"; 
            life per person in "life_expectancy_years.csv"
            children per woman in "children_per_woman_total_fertility.csv"
            contry and area diction in "contry_and_area.csv"
            TODO: more datasets....
        """
        
        if start_years>end_years:
            raise Exception("the start year must be smaller than the end year")
            #make sure that years condition to be correct
        
        file_path = os.path.join(DATADIR, data_file_name)
        csvfile = csv.reader(open(file_path,'r'))
        #read the csvfile and store them in memory
        
        
        
        if DATADIR is None:
            raise Exception("please specify the file direction in the third input")
        # in case the DATADIR is removed    
            
        if (start_years < min_year or len(next(csvfile))+ min_year - 2<end_years):
            raise Exception("input year range exceeds the data")
        # see if the input years are out of the range in the data


        contrydata = np.array(
            [rows[(start_years - min_year + 1):(end_years - min_year + 2)] 
            for rows in csvfile if rows[0] == self.name]
            )        


        if len(contrydata) == 0:# or len(contrydata) == 0:
            return ["-20.0"]#move out from the screen

        if contrydata == "":
            return ["-20.0"]#move out from the screen

        else:
            return contrydata
        #in this "ifcondition", usurally there is only one match, so take the first elements in that list, 
        #and transform it into an nparray

    def get_population_data_in_oneyear(self, years, presented_population_data_unit = 1):
        #extract one year data method, might be redundent
        self.population_total = int(self.exract_data_fromcsv(years, years)[0])
        self.population_data_unit = presented_population_data_unit
        #numbers are presented in unit 1, might be million, billion

    def get_fertility_in_oneyear(self, years):
        return float(self.exract_data_fromcsv(years, years, data_file_name ="children_per_woman_total_fertility.csv")[0])

    def get_lifeexpect_in_oneyear(self, years):
        return float(self.exract_data_fromcsv(years, years,data_file_name ="life_expectancy_years.csv")[0])

    def get_GINI_index_in_oneyear(self, years):
        return float(self.exract_data_fromcsv(years, years,data_file_name ="Gini_by_contry.csv")[0])/100

    def get_GDPperCap_in_oneyear(self, years):
        return float(self.exract_data_fromcsv(years, years,data_file_name ="GDP_per_capita.csv")[0])

    '''
    #Version 1:
    def get_both_fertandlife_point(self, years):
        return np.array([self.get_lifeexpect_in_oneyear(years),self.get_fertility_in_oneyear(years) ,0])
    '''

    #Version 2: used in Danim\video1\4MoreComparison.py line 97
    def get_both_fertandlife_point(self, years):
        GDPperCap = self.get_GDPperCap_in_oneyear(years)
        log_factor = 250
        log_base = 2
        #print(self.name,GDPperCap)
        origin_x_GDPperCap = math.log(np.divide(GDPperCap,log_factor),log_base)
        
        return np.array([origin_x_GDPperCap, self.get_lifeexpect_in_oneyear(years), 0])


    def get_transfromed_fertandlife_point(self, years):
        return np.array(coordinate_origin_to_new(self.get_both_fertandlife_point(years)))

        
#SHAPES:

#1. CIRCLE



    def set_the_contry_circle(self, color= RED,opacity=0.3,show_CN_pop_lable = False):
        
        if not hasattr(self, "population_total"):
            raise Exception("the contry object has no data yet, should use exract_data_fromcsv method first")

        self.shape = Circle(radius = math.sqrt(self.population_total*self.population_data_unit/1000000000*population_per_circle_area/np.pi))
        self.shape.set_color(color)
        self.shape.set_fill(color,opacity)

        if self.circleconfig["show_contry_name"] is True:

            if self.show_CN_name:
                self.contry_name = TextMobject(self.CN_name)
            else:
                self.contry_name = TextMobject(self.name)

            self.contry_name.next_to(self.shape, UP)

        if self.circleconfig["show_population_lable"] is True:
            contry_population_data = self.population_total*self.population_data_unit

            if not show_CN_pop_lable:#英文人口标签
                self.population_lable = DecimalNumber(
                    contry_population_data/1000000000,
                    show_ellipsis=False,
                    num_decimal_places=1,
                    include_sign=False
                )


                self.align_contry_lable_close_to_circle(lable_type = "population_lable", direction_alpha = - PI/4, buff = 0.2,scale_factor = self.circleconfig["numbers_scale_factor"])
                self.population_lable.set_value(contry_population_data/1000000000)

                if contry_population_data < 1000000000:
                    self.population_lable_unit = TextMobject("Million")
                    self.population_lable.set_value(contry_population_data/1000000)   
                else:
                    self.population_lable_unit = TextMobject("Billion")

            if show_CN_pop_lable:#中文人口标签
                self.population_lable = DecimalNumber(
                    contry_population_data/100000000,
                    show_ellipsis=False,
                    num_decimal_places=1,
                    include_sign=False
                )                


                self.align_contry_lable_close_to_circle(lable_type = "population_lable", direction_alpha = - PI/4, buff = 0.2,scale_factor = self.circleconfig["numbers_scale_factor"])
                self.population_lable.set_value(contry_population_data/100000000)

                if contry_population_data < 100000000:
                    self.population_lable_unit = TextMobject("百万")
                    self.population_lable.set_value(contry_population_data/1000000)   
                else:
                    self.population_lable_unit = TextMobject("亿")


            self.population_lable_unit.scale(self.circleconfig["numbers_scale_factor"])
            self.population_lable_unit.add_updater(lambda d: 
                d.next_to(self.population_lable,
                self.circleconfig["distance_between_lable_and_unit"]))

    def switch_population_lable(self):
        if self.circleconfig is not None:
            if self.circleconfig["show_population_lable"] is not True:
                self.circleconfig["show_population_lable"] = True
            else:
                self.circleconfig["show_population_lable"] = False


    def switch_contry_name(self):
        if self.circleconfig is not None:
            if self.circleconfig["show_contry_name"] is True:
                self.circleconfig["show_contry_name"] = False        

            else:
                self.circleconfig["show_contry_name"] = True            


    def switch_name_and_poplable(self):
        self.switch_contry_name()
        self.switch_population_lable()

    def fill_data_and_set_the_circle(self,years=2018,color=RED,switch_on = True, show_CN_pop_lable = False):

        if switch_on == True:
            self.switch_name_and_poplable()
        self.get_population_data_in_oneyear(years)
        self.set_the_contry_circle(color,show_CN_pop_lable = show_CN_pop_lable)

    def fill_data_set_the_circle_then_group(self,years=2018,color=RED,switch_on = True, show_CN_pop_lable = False):
        self.fill_data_and_set_the_circle(years,color,switch_on, show_CN_pop_lable = show_CN_pop_lable)
        if hasattr(self, "population_lable"):
            return VGroup(self.shape,self.contry_name,self.population_lable,self.population_lable_unit)
        else:
            if not self.show_CN_name:
                self.contry_name = TextMobject(self.name)
            else:
                self.contry_name = TextMobject(self.CN_name)
            self.contry_name.next_to(self.shape, UP)
            return VGroup(self.shape,self.contry_name)


#Circle_lables:
    def create_data_coordinate_lable(self, years, lable_color = RED, position_func = lambda lable,circle:lable.next_to(circle,RIGHT,buff = 0.001) , lable_scale_factor = 0.6):
        target_circle = self.shape.copy()
        if hasattr(self, "shape"):
            self.data_x_lable =DecimalNumber(
                coordinate_new_to_origin(self.shape.get_center())[0],
                num_decimal_places=1,
                group_with_commas=False
                )

            self.data_y_lable =DecimalNumber(
                coordinate_new_to_origin(self.shape.get_center())[1],
                num_decimal_places=1,
                group_with_commas=False
                )
      
            data_lable_left = TextMobject("(",tex_to_color_map={"(": lable_color})
            position_func(data_lable_left,self.shape)
            self.data_x_lable.next_to(data_lable_left,RIGHT,buff=0.1)

            data_lable_comma =  TextMobject(",",tex_to_color_map={",": lable_color})
            data_lable_comma.next_to(self.data_x_lable,RIGHT,buff=0.06)
            data_lable_comma.scale(0.8)
            data_lable_comma.shift(0.2*DOWN)        

            self.data_y_lable.next_to(self.data_x_lable,RIGHT,buff=0.18,)

            data_lable_right = TextMobject(")",tex_to_color_map={")": lable_color})
            data_lable_right.next_to(self.data_y_lable,RIGHT,buff=0.1,)


            self.data_coordinate_lable = VGroup(
                    data_lable_left,
                    data_lable_comma,
                    data_lable_right
                    ).scale(lable_scale_factor)
            self.data_x_lable.scale(lable_scale_factor,about_point = self.data_coordinate_lable.get_center())
            self.data_y_lable.scale(lable_scale_factor,about_point = self.data_coordinate_lable.get_center())


    def align_contry_lable_close_to_circle(self,lable_type = 'contry_name', direction_alpha = PI*5/4, buff = 0.1,scale_factor = 0.3):
        
        if hasattr(self,lable_type):
            lable = getattr(self,lable_type)
            lable.scale(scale_factor)

            lable.shift(
                get_circle_critical_point(self.shape, direction_alpha, buff) - 
                lable.get_critical_point(np.array([np.cos(direction_alpha + PI),np.sin(direction_alpha +PI),0])))

    def get_the_namelable_circle_alignment_animation(self,direction_alpha = PI*5/4, buff_used = 0.1,scale_factor = 0.3):
        if hasattr(self,"contry_name"):

            lable_new = self.contry_name.copy()
            self.contry_name.scale(scale_factor)
            self.contry_name.shift(
                get_circle_critical_point(self.shape, direction_alpha, buff_used) - 
                self.contry_name.get_critical_point(np.array([np.cos(direction_alpha + PI),np.sin(direction_alpha +PI),0])))
            #lable_new, lable = lable,lable_new            
            return ReplacementTransform(lable_new,self.contry_name)


# Distribution shape function:

    def set_the_contry_distribution(
        self, 
        year, 
        color= RED, 
        opacity=DEFAULT_DISTRIBUTION_OPACITY,
        confidence_interval = DEFAULT_CONFIDENCE_INTERVAL, 
        show_CN_pop_lable = False,
        x_axis = NumberLine(x_min = -8,x_max = 8)#redundant variable, just in case
        ):
        
        #calculate the income distribution with following assumption:
        #1. income distribution follows log normal 
        #2. the income mean is estimated by GDP per capita(use the 2011 price level)
        #3. the income is measured by The Geary–Khamis dollar, more commonly known as the international dollar
        #4. the variance is estimated by Gini index(an indication for income inequality)
        
        #get the raw data
        Gini = self.get_GINI_index_in_oneyear(year)
        GDP_per_capita = self.get_GDPperCap_in_oneyear(year)/num_of_days_per_year
        #calculate the mean&std for lognormal distribution variable with the log base e and log factor 1
        std = np.sqrt(2)*inverse_of_normal_cdf((Gini + 1. )/ 2.)
        mean = np.log(GDP_per_capita) - 1./2.*np.square(std)

        #adjust the variable to the LOG_BASE and LOG_FACTOR
        #adjust the GDP_per_capita to income per capita per day
        mean = (mean - np.log(LOG_FACTOR))/(np.log(LOG_BASE))
        std = std/np.log(LOG_BASE)
        #the x_axis must be log scale:
        self.shape = NormalDistribution(
            mean = mean,
            std = std,
            confidence_interval = confidence_interval,
            color = color,
            fill_color = color,
            fill_opacity = opacity,
            set_up_the_bot_curve = True
            )

        #adjust the hights according to its population:
        self.shape.height_adjust_factor = (
            float(
                self.exract_data_fromcsv(
                    year, year)[0]
                )/1000000000
            )*population_per_distribution_area / self.shape.confidence_interval

        self.shape.points[:,1] *= self.shape.height_adjust_factor


    def get_stack_over_animation(self,distribution):
        new_dis = self.shape.deepcopy()
        self.shape,new_dis = new_dis,self.shape
        self.shape.stack_over(distribution)
        return ReplacementTransform(new_dis,self.shape)

    def update_the_contry_distribution(self,new_year,axes = Axes()):

        #get the raw data
        Gini = self.get_GINI_index_in_oneyear(new_year)
        GDP_per_capita = self.get_GDPperCap_in_oneyear(new_year)/num_of_days_per_year
        #calculate the mean&std for lognormal distribution variable with the log base e and log factor 1
        std = np.sqrt(2)*inverse_of_normal_cdf((Gini + 1. )/ 2.)
        mean = (np.log(GDP_per_capita) - 1./2.*np.square(std))        

        #adjust the variable to the LOG_BASE and LOG_FACTOR
        #adjust the GDP_per_capita to income per capita per day
        mean = (mean - np.log(LOG_FACTOR))/(np.log(LOG_BASE))
        std = std/np.log(LOG_BASE)

        #the x_axis must be log scale:
        shape = NormalDistribution(
            mean = mean,
            std = std,
            confidence_interval = DEFAULT_CONFIDENCE_INTERVAL,
            color = self.shape.color,
            fill_color = self.shape.color,
            fill_opacity = DEFAULT_DISTRIBUTION_OPACITY,
            set_up_the_bot_curve = True
            )


        #adjust the hights according to its population:
        shape.height_adjust_factor = (
            float(
                self.exract_data_fromcsv(
                    new_year, new_year)[0]
                )/1000000000
            )*population_per_distribution_area / self.shape.confidence_interval

        shape.points[:,1] *= shape.height_adjust_factor
        '''
        end_point = x_axis.number_to_point(shape.mean)
        start_point = np.array([shape.mean,0,0])
        shift_vec = end_point - start_point
        shape.shift(shift_vec)
        '''
        shape.fit_to_new_axes(axes)
        return shape

    def get_update_single_contry_distribution_animation(self,new_year,axes):
        new_shape = self.update_the_contry_distribution(new_year,axes = axes)
        self.shape,new_shape = new_shape,self.shape
        return ReplacementTransform(new_shape,self.shape)

#UPDATE_FUNCTION:

    def update_the_circle_radius(self,years,update_the_radius = True):
        if isinstance(self.shape, Circle):
            old_pop = self.population_total
            if update_the_radius:
                self.get_population_data_in_oneyear(years)
                circle_scale_factor = math.sqrt(self.population_total/old_pop)
                self.shape.radius *= circle_scale_factor
            else:
                new_pop = int(self.exract_data_fromcsv(years, years)[0])
                circle_scale_factor = math.sqrt(new_pop/old_pop)

            return circle_scale_factor


    def update_populaton_lable_by_year_animation(self,new_year,show_population_lable_in_graph = False):
        if show_population_lable_in_graph and hasattr(self,"population_lable"):

            shift_vector = self.get_transfromed_fertandlife_point(new_year) - self.shape.get_center()
            pop_num = int(self.exract_data_fromcsv(new_year, new_year)[0])
            population_lable_new = self.population_lable.copy()
            population_lable_new.shift(shift_vector)

            #todo: add cn_poplable update
            if pop_num < 1000000000:

                population_lable_new.set_value(pop_num/1000000)
                population_lable_unit_new = TextMobject("Million")

            else:
                population_lable_new.set_value(pop_num/1000000000)
                population_lable_unit_new = TextMobject("Billion")

            population_lable_unit_new.scale(self.circleconfig["numbers_scale_factor"])
            population_lable_unit_new.next_to(population_lable_new, self.circleconfig["distance_between_lable_and_unit"])

            population_lable_new,self.population_lable = self.population_lable,population_lable_new
            population_lable_unit_new, self.population_lable_unit = self.population_lable_unit, population_lable_unit_new

            return AnimationGroup(
                ReplacementTransform(population_lable_new,self.population_lable),
                ReplacementTransform(population_lable_unit_new,self.population_lable_unit)
                )

        else:
            pass
            #raise Exception("missing key attributes for the Contry class, might be population_lable, or assign show_population_lable_in_graph to True")


    def update_circlelable_by_year_animation(self,new_year,default_buff = 0.1,lable_direction_angle = 0):
        if hasattr(self,"data_coordinate_lable") and hasattr(self,"shape"):

            '''
            self.data_coordinate_lable = VGroup(
                    data_lable_left, #------ 0
                    data_lable_comma, #------ 1
                    data_lable_right #------ 2
                    ).scale(lable_scale_factor)
            '''

            data_x_lable_new = self.data_x_lable.copy()

            data_x_lable_new.set_value(self.get_both_fertandlife_point(new_year)[0])
            data_y_lable_new = self.data_y_lable.copy()
            data_y_lable_new.set_value(self.get_both_fertandlife_point(new_year)[1])
            #Create new x y coordinate lables

            shift_vector = self.get_transfromed_fertandlife_point(new_year) - self.shape.get_center()
            #adjust_vec = np.array([np.cos(lable_direction_angle),np.sin(lable_direction_angle),0])*(self.update_the_circle_radius(new_year,update_the_radius = False)-1)*self.shape.get_width()/2#adjust the lable so it's always next to the edge of the circle

            #Where to move

            data_x_lable_new.shift(shift_vector)#+adjust_vec)
            data_y_lable_new.shift(shift_vector)#+adjust_vec)
            data_x_lable_new, self.data_x_lable = self.data_x_lable, data_x_lable_new
            data_y_lable_new, self.data_y_lable = self.data_y_lable, data_y_lable_new

            return AnimationGroup(
                ReplacementTransform(data_x_lable_new,self.data_x_lable),
                ReplacementTransform(data_y_lable_new,self.data_y_lable))

        else:
            raise Exception("missing key attributes for the Contry class, might be data_coordinate_lable or circle shape")

    def update_circle_by_year_animation(self,new_year, show_track = False):# show_name_lable = False):
        if isinstance(self.shape,Circle):
            circle_new = self.shape.copy()

            circle_new.scale(self.update_the_circle_radius(new_year))
            circle_new.move_to(self.get_transfromed_fertandlife_point(new_year))
            circle_new,self.shape = self.shape,circle_new
            if show_track:
                return Transform(circle_new,self.shape)
            else:
                return ReplacementTransform(circle_new,self.shape)
        else:
            raise Exception("the shape is not a circle")

    def update_the_circle_with_everything_turnon_animation(self,new_year,show_track = False,show_population_lable_in_graph = False,lable_direction_angle = PI*5/4):

        if hasattr(self,'shape') and hasattr(self,'data_coordinate_lable') and hasattr(self,'contry_name'):#and hasattr(self,'population_total') and 
            shift_vec = self.get_transfromed_fertandlife_point(new_year) - self.shape.get_center()            
            adjust_vec = np.array([np.cos(lable_direction_angle),np.sin(lable_direction_angle),0])*(self.update_the_circle_radius(new_year,update_the_radius = False)-1)*self.shape.get_width()/2#adjust the lable so it's always next to the edge of the circle

            AnimGroup=AnimationGroup(
                self.update_circlelable_by_year_animation(new_year),
                self.update_populaton_lable_by_year_animation(new_year,show_population_lable_in_graph),
                self.update_circle_by_year_animation(new_year,show_track),
                ApplyMethod(self.contry_name.shift,shift_vec+adjust_vec),
                ApplyMethod(self.data_coordinate_lable.shift,shift_vec)
                )
            return AnimGroup
        else:
            raise Exception("missing key Contry.attributes, might be one of the following: shape, data_coordinate_lable, population_total or contry_name")

    def update_contry_name_lable(self,new_year,lable_direction_angle = PI*5/4):

        shift_vec = self.get_transfromed_fertandlife_point(new_year) - self.shape.get_center()            
        adjust_vec = np.array([np.cos(lable_direction_angle),np.sin(lable_direction_angle),0])*(self.update_the_circle_radius(new_year,update_the_radius = False)-1)*self.shape.get_width()/2#adjust the lable so it's always next to the edge of the circle
            
        return ApplyMethod(self.contry_name.shift,shift_vec+adjust_vec)
                



class Area():

    def __init__(self,areaname = None,init_by_areaname = True, contry_list = None,show_CN_name = False):

        if init_by_areaname:
            self.areaname = areaname
            self.contry_name_list = []
            self.contry_list = []

            # in case the DATADIR is removed
            if DATADIR is None:
                raise Exception("please specify the file direction in Contry.py")

            # GET the contry names in the area:
            area_file_path = os.path.join(DATADIR, contry_and_area_file)
            csvfiles = csv.reader(open(area_file_path,'r'))
            #read the csvfile and store them in memory

            # generate the list that contains all the contry names in that area 
            for row in csvfiles:
                if row[1] == self.areaname:
                    #line 780 and 781 is used in Danim\video1\4MoreComparison.py line 97
                    if row[0] in ["Holy See","Liechtenstein"]:
                        continue
                    self.contry_name_list.append(row[0])
                    self.contry_list.append(Contry(row[0],show_CN_name = show_CN_name))

            self.num_of_contries = len(self.contry_name_list)

        #initialize by a list of contry objects, the input contry_list must be a list of contries
        #this way of initialization is used specifically for stacked contry distributions updates
        #Like the input argument in NDGroup, you must specify the list order from bottom contry to 
        #the top contry
        else:
            assert(isinstance(contry_list,list))
            self.contry_list = contry_list



    #functions are used for init_by_areaname(for circle or bubble charts update):
    def generate_all_contry_circles(self,years_date =2018,COLORMAT = [RED], if_switch_on = False, Axes = None,sort_by_axes = False):

        # color_fill_method can be a single color or a list of colors, but the number of that list must equal self.num_of_contries
        if len(COLORMAT) == 1:
            color_to_fill = COLORMAT*self.num_of_contries
        elif len(COLORMAT) == self.num_of_contries:
            color_to_fill = COLORMAT

        else:
            raise Exception("the number of colors you assigned does not match the number of contries within that area")

        #check if creation animation is in "sort by axes"mode:
        if sort_by_axes and (Axes is not None): 

            y0 = Axes.x_axis.number_to_point(Axes.x_axis.x_max)[1]
            grow_time = 0.5
            transfer_run_time = 0.5
            fadeout_time = 0.3
            self.grow_animations = []
            self.transform_animations = []

            for index,contry in enumerate(self.contry_list):

                contry.fill_data_and_set_the_circle(years_date,color_to_fill[index],if_switch_on)

                if hasattr(contry,"contry_name"):
                    contry.contry_name.scale(0.3)
                    contry.contry_name.next_to(contry.shape,RIGHT)
                    contryG = VGroup(contry.shape,contry.contry_name)

                    if index == 0:
                        previous_contry = contry
                        cornor_contry = contry
                        

                    height = contryG.get_critical_point(UP)[1] - contryG.get_critical_point(DOWN)[1]
                    cell = previous_contry.shape.get_critical_point(DOWN)[1]

                    if index == 0:
                        contryG.shift(3*RIGHT + 3*UP)

                    elif cell - height < y0 + 0.5:
                        contryG.next_to(cornor_contry.shape,LEFT)
                        contryG.shift(0.25*LEFT)
                        cornor_contry = contry

                    else:
                        contryG.next_to(
                            VGroup(
                                previous_contry.shape,
                                previous_contry.contry_name
                                ),
                            DOWN
                            )

                    self.grow_animations.append(GrowFromCenter(contryG,run_time = grow_time))
                    self.transform_animations.append(
                        AnimationGroup(
                            ApplyMethod(
                                contry.shape.move_to,
                                contry.get_transfromed_fertandlife_point(years_date),
                                run_time = transfer_run_time
                                ),
                            FadeOut(contry.contry_name,run_time = fadeout_time),
                            lag_ratio = 0.2
                            )
                        )

                    previous_contry = contry


                else:
                    raise Exception("in sort_by_axes mode, the contry objects must have attribute contry_name")
        
        #if creation animation is not in "sort by axes"mode:
        # the contry circles will be shown at the GrowFromCenter()
        else:
            for index,contry in enumerate(self.contry_list):
                contry.fill_data_and_set_the_circle(years_date,color_to_fill[index],if_switch_on)
                contry.shape.move_to(contry.get_transfromed_fertandlife_point(years_date))

                

    def get_creation_animation(self, show_name_lable = False,sort_by_axes = False):
        if hasattr(self,"contry_list"):
            anim = []
            if sort_by_axes:
                anim.append(AnimationGroup(*self.grow_animations,lag_ratio = 0.2))

            else:
                for i in self.contry_list:
                    anim.append(GrowFromCenter(i.shape))
                if show_name_lable:
                    for i in self.contry_list:
                        anim.append(Write(i.contry_name))

            return anim
        else:
            return None

    def update_area_circles_by_year_animation(self,new_year, show_tracks = False, show_names = False):
        anim_group = []
        for contry in self.contry_list:
            anim_group.append(contry.update_circle_by_year_animation(new_year, show_tracks))
        return anim_group

    def update_area_contryname_by_year_animation(self,new_year,lable_direction_angle = PI*5/4):
        anim_group = []
        for contry in self.contry_list:
            if contry.show_contry_name_lable:
                anim_group.append(contry.update_contry_name_lable(new_year,lable_direction_angle))
        return anim_group

    #functions are used for init_by_contrylist:
    def update_stacked_distributions_by_year_animation(self,new_year,axes = Axes()):

        #version 2
        origin_group = VGroup()
        new_group = VGroup()

        for i,contry in enumerate(self.contry_list):
            origin_shape = contry.shape
            new_shape = contry.update_the_contry_distribution(new_year,axes)

            if i == 0:
                dis_groups = NDGroup(new_shape)
            else:
                new_shape.stack_over(dis_groups)
                dis_groups = NDGroup(dis_groups,new_shape)
            contry.shape,new_shape = new_shape,contry.shape
            origin_group.add(new_shape)
            new_group.add(contry.shape)

        animations= ReplacementTransform(origin_group,new_group)

        return animations


        '''
        animations = [] 

        for i,contry in enumerate(self.contry_list):
            origin_shape = contry.shape
            new_shape = contry.update_the_contry_distribution(new_year,axes)

            if i == 0:
                dis_groups = NDGroup(new_shape)
            else:
                new_shape.stack_over(dis_groups)
                dis_groups = NDGroup(dis_groups,new_shape)
            contry.shape,new_shape = new_shape,contry.shape
            animations.append(ReplacementTransform(new_shape,contry.shape))

        Grouped_animation = AnimationGroup(*animations)



        #Animation = AnimationGroup(ShowCreation(original_shape),FadeOut(new_shape))
        return Grouped_animation
        #update_the_contry_distribution(self,new_year,x_axis = NumberLine(x_min = -8,x_max = 8)):
        '''
