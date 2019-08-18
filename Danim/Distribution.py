from manimlib.constants import *

import itertools as it
import numpy as np
import math
from scipy.stats import norm
import copy

from manimlib.mobject.mobject import Mobject
from manimlib.mobject.types.vectorized_mobject import VGroup
from manimlib.mobject.types.vectorized_mobject import VMobject
from manimlib.mobject.number_line import NumberLine
from manimlib.mobject.coordinate_systems import Axes
from manimlib.utils.config_ops import digest_config
from manimlib.utils.bezier import bezier,interpolate,get_smooth_handle_points
from manimlib.utils.space_ops import get_norm
from manimlib.utils.config_ops import merge_dicts_recursively
from manimlib.mobject.numbers import DecimalNumber


class LogscaleNumberLine(NumberLine):

#create a logscale numberline, 
#with new_x = factor * base ^ (origin_x)
#it's important to understand the difference 
#between origin_x(which is coordinates on screen) and 
#the new_x (which is the number shown on screen)

#e.g. you want to create a numberline 
#contain evenly distributed marks [3,30,300,3000]
#then the origin_x is [0,1,2,3]
#the new_x is [3,30,300,3000]
#log_factor = 3
#log_base = 10


    CONFIG = {
        "leftmost_tick" : 0,#the origin_x
        "is_log_scale" : True,
        "number_scale_val": 0.7,
        "log_factor": 1,
        "log_base":10,
        "x_min": 0, #the origin_x
        #"include_scaled_numbers": True 
        }


    def __init__(self, **kwargs):
        digest_config(self, kwargs)
        self.number_at_center = self.log_factor
        NumberLine.__init__(self,**kwargs)

    def number_to_point(self, number, number_is_origin_x = True):
        
        #if input number is new_x 
        if not number_is_origin_x:
            number = math.log(np.divide(number,self.log_factor),self.log_base)

        alpha = float(number - self.x_min) / (self.x_max - self.x_min)
        return interpolate(
            self.get_start(), self.get_end(), alpha
        )

    def point_to_number(self, point, to_origin_x_number = True):

        start_point, end_point = self.get_start_and_end()
        full_vect = end_point - start_point
        unit_vect = normalize(full_vect)

        def distance_from_start(p):
            return np.dot(p - start_point, unit_vect)

        proportion = fdiv(
            distance_from_start(point),
            distance_from_start(end_point)
        )
        origin_x = interpolate(self.x_min, self.x_max, proportion)

        if to_origin_x_number:
            return origin_x
        else:
            return self.log_factor * (self.log_base ** (origin_x))#new_x

    def get_number_mobject(self, number,# input number should be a origin_x
                           number_config=None,
                           scale_val=None,
                           direction=None,
                           buff=None,
                           number_is_origin_x = True):
        number_config = merge_dicts_recursively(
            self.decimal_number_config,
            number_config or {},
        )
        if scale_val is None:
            scale_val = self.number_scale_val
        if direction is None:
            direction = self.label_direction
        buff = buff or self.line_to_number_buff

        num_mob = DecimalNumber(self.log_factor * (self.log_base ** (number)), **number_config)
        num_mob.scale(scale_val)
        num_mob.next_to(
            self.number_to_point(number,number_is_origin_x),
            direction=direction,
            buff=buff
        )
        return num_mob    


# 全局变量:

# be careful with this variable, might affect the speed dramatically
NUM_OF_INTERATIONS_IN_ESTIMATION = 30

# 全局方法：

#list-sorting alg, from small to big
def bubble_sort(alist):
    length = len(alist)
    for i in range(length - 1):
        # i represents how many rounds of comparison has done
        for j in range(length - i - 1):
            if alist[j] > alist[j + 1]:
                alist[j], alist[j + 1] = alist[j + 1], alist[j]

#points sorting alg, from small to big
def sort_points_by_x(points):
    sort_index = np.argsort(points,axis=0)[:,0]
    result = np.zeros((len(points),3))
    for i,index in enumerate(sort_index):
        result[i] = points[index]
    return result

def normal_pdf(x, mean = 0, std = 1):
    variance = np.square(std)
    exp_factor = 1/(np.sqrt(2*PI*variance))
    exponent = - (np.square(x - mean))/(2* variance)
    return exp_factor*np.exp(exponent)

def normal_pdf_custom(x, mean = 1.29, std = 1):
    variance = np.square(std)
    exp_factor = 1/(np.sqrt(2*PI*variance))
    exponent = - (np.square(x - mean))/(2* variance)
    return exp_factor*np.exp(exponent)

def lognormal_pdf(x,mean = 1.63,std = 1):
    factor = 1./(x*std*np.sqrt(2*PI))
    exponent = - (np.square(np.log(x) - mean))/(2*np.square(std))
    return factor*np.exp(exponent)

def normal_cdf(x, mean = 0, std = 1):
    return 1/2*(1+ math.erf((x-mean)/(std*np.sqrt(2))))

def inverse_of_normal_cdf(probability):
    return norm.ppf(probability)

def apply_function_to_points_smoothly(points, func, mean = 0, std = 1, about_point = ORIGIN):
    # this function takes care about the smootheness of each curve
    # the func is apply along y_axis( which means the input is x, output is y)

    #apply function to anchor points
    anchors = points[::3]
    anchors -= about_point
    anchors[:,1] = func(anchors[:,0],mean,std) # x to y, func's input is number not point
    anchors += about_point

    # get smooth handles points
    h1, h2 = get_smooth_handle_points(anchors)

    # insert anchors and handles accordingly
    points[0] = anchors[0]
    arrays = [h1, h2, anchors[1:]]
    for index, array in enumerate(arrays):
        points[index + 1::3] = array

    return points

def is_over_lap(A_min,A_max,B_min,B_max):
	# Two range A & B, if no overlap, return False, and empty list
	# if there are overlap, return True and the overlap range list 
	# with two elements: overlap start and overlap end.

	is_overlap = (min(A_max,B_max) - max(A_min,B_min) > 0)

	if is_overlap:
		overlap = [max(A_min,B_min),min(A_max,B_max)]
	else:
		overlap = []

	return is_overlap, overlap


def is_in_range(x, range_min, range_max, include_edge = False):
    # min&max input order dose not matter
    if not include_edge:
        if x >= max(range_min,range_max) or x <= min(range_max,range_min):
            return False
        else:
            return True

    if include_edge:
        if x > max(range_min,range_max) or x < min(range_max,range_min):
            return False
        else:
            return True



class NormalDistribution(VMobject):
    CONFIG = {
    	#distribution config:
    	"confidence_interval":0.99,
    	"mean": 0,
    	"std":1,

        # the shape is designed to be closed form, 
        # so there is the bottom curve
        "num_of_anchor_in_up_curve": 61,
        # the num_of anchors in up curve must be odd 
        "num_of_anchor_in_bottom_curve": 60,
        #better less one point than up curve anchors,
        #if you do so, it has a very nice property that
        #each up curve anchor will match a bot curve anchor
        # with the same x_axis value

        "stack_mode" : False,
        "set_up_the_bot_curve":False,
        }

    def __init__(self,**kwargs):

        digest_config(self, kwargs)
        self.pdfunction = normal_pdf
        if not self.set_up_the_bot_curve:
            self.num_of_anchor_in_bottom_curve = 0
        #determin x_max and x_min
        side_probability = (1. - self.confidence_interval)/2
        self.x_max = self.std * (inverse_of_normal_cdf(side_probability + self.confidence_interval)) + self.mean
        self.x_min = self.std * (inverse_of_normal_cdf(side_probability)) + self.mean
        
        VMobject.__init__(self,**kwargs)
        self.highest_points = self.get_highest_point()

    def generate_points(self):

        # set up the up_curve points:
        self.num_of_up_points =  3 * self.num_of_anchor_in_up_curve - 2 
        up_curve_points = np.zeros((self.num_of_up_points,self.dim))
        up_curve_points[:, 0] = np.linspace(
            self.x_min, self.x_max, self.num_of_up_points
            )

        apply_function_to_points_smoothly(up_curve_points, self.pdfunction, self.mean, self.std)
        # this function automatically takes care of the  
        # handle points so that the up curve is soomthy
        #shift down to touch the x_axis:
        shift_vec = up_curve_points[0][1] * DOWN
        up_curve_points += shift_vec

        # set up the bot_curve points:
        if self.set_up_the_bot_curve:
            self.number_of_bot_points = 3 *self.num_of_anchor_in_bottom_curve + 1 # +1多添加了一个点
            bot_curve_points = np.zeros((self.number_of_bot_points,self.dim))

            #如果用np.linspace(self.x_max,self.x_min,self.number_of_bot_points)，上下点的x值会稍有不同
            bot_curve_points[:,0] = up_curve_points[:, 0][::-1]


            bot_curve_points = np.delete(bot_curve_points, 0 ,axis = 0)# 删去多添加的那个点
            self.number_of_bot_points -= 1

            #integrate whole points
            self.points = np.append(up_curve_points,bot_curve_points, axis = 0)
        else:
            self.number_of_bot_points = 0
            self.points = up_curve_points        

    def determine_x_max_min_by_confidence_interval(self):

        side_probability = (1. - confidence_interval)/2
        self.x_max = self.std * (inverse_of_normal_cdf(side_probability + confidence_interval)) + self.mean
        self.x_min = self.std * (inverse_of_normal_cdf(side_probability)) + self.mean
        return self

    def get_mean_point(self):

        up_curve_anchors = self.get_up_curve_anchors()
        return np.divide((up_curve_anchors[0] + up_curve_anchors[-1]),2)



    def get_up_curve_anchors(self):
        return self.points[0:self.num_of_up_points:3]

    def get_up_curve_points(self):
    	return self.points[0:self.num_of_up_points]

    def set_up_curve_points(self,points):
    	if len(points) == len(self.get_up_curve_points()):
    		self.points[0:self.num_of_up_points] = points

    def get_up_curve_points(self,include_first_one = True):
        return self.points[0:self.num_of_up_points]

    def get_bot_curve_anchors(self,include_first_one = False):
        #missing the first anchor, it belongs to the end points in up curve
        if include_first_one:
            return self.points[self.num_of_up_points-1::3]
        else:
            return self.points[self.num_of_up_points+2::3]

    def get_distribution_value_by_x(self,x,get_up_curve_value = True, num_of_iterations = NUM_OF_INTERATIONS_IN_ESTIMATION):
        # the more number of iterations, the more accurate the value will be
        if not is_in_range(x,self.x_min,self.x_max,include_edge = True):
            raise(Exception("the input x is not within the range of the distribution"))

        if get_up_curve_value:
            align_points = self.get_up_curve_anchors()

            for i in range(len(align_points)-1):
                if is_in_range(x,align_points[i][0],align_points[i+1][0],include_edge = True):

                    func = self.get_nth_curve(i)
                    point_on_curve = func(0)
                    for k in range(0,num_of_iterations):
                        new_point = func(k/num_of_iterations)
                        if abs(new_point[0] - x) <= abs(point_on_curve[0] - x):
                            point_on_curve = new_point           
                    break
            return point_on_curve[1]

        elif self.set_up_the_bot_curve:
            align_points = self.get_bot_curve_anchors(include_first_one = True)
            for i in range(len(align_points)-1):
                if is_in_range(x,align_points[i][0],align_points[i+1][0],include_edge = True):
                    j = i+self.num_of_anchor_in_up_curve-1
                    func = self.get_nth_curve(j)
                    point_on_curve = func(0)
                    for k in range(0,num_of_iterations):
                        new_point = func(k/num_of_iterations)
                        if abs(new_point[0] - x) <= abs(point_on_curve[0] - x):
                            point_on_curve = new_point                           
                    break
            return point_on_curve[1]


    def get_highest_point(self, to_specific_axis = False):
        if self.stack_mode == False and not to_specific_axis:
            if self.num_of_anchor_in_up_curve%2 == 0:
                return self.get_up_curve_anchors()[(self.num_of_anchor_in_up_curve - 1)/2]
            else:
                return np.array([
                    (self.x_min+self.x_max)/2,
                    self.get_distribution_value_by_x((self.x_min+self.x_max)/2),
                    0])

    def insert_new_anchor_by_x(self,x,anchors, multiple_xs = False):
        # use the function is_in_range(x, range_min, range_max):
        a = 0 #position adjustor
        num_of_up_anchors = self.num_of_anchor_in_up_curve #counter
        num_of_bot_anchors = self.num_of_anchor_in_bottom_curve #counter
        index = [] # variable that stores the position index information
        old_anchors = copy.deepcopy(anchors)

        # if there is only one value of x to insert 
        if not multiple_xs:
            if not x in anchors[:,0]:
                for i in range(len(anchors)-1):
                    if is_in_range(x, anchors[i][0],anchors[i+1][0]):
                        index.append(i)

            for i in index:
                if i < self.num_of_anchor_in_up_curve - 1:
                    T = (x - min(old_anchors[i][0],old_anchors[i+1][0]))/(abs(old_anchors[i][0] - old_anchors[i+1][0]))
                    num_of_up_anchors += 1
                else:
                    T = (max(old_anchors[i][0],old_anchors[i+1][0])-x)/(abs(old_anchors[i][0] - old_anchors[i+1][0]))
                    num_of_bot_anchors += 1

                new_anchor_point = self.get_nth_curve(i)(T)
                anchors = np.insert(anchors,i+a+1,new_anchor_point,axis = 0)
                a += 1

        # insert multiple xs, x must be a list        
        elif isinstance(x,list):
            bubble_sort(x)
            xs = []
            for x_cood in x:
                if not x_cood in anchors[:,0]:
                    for i in range(len(anchors)-1):
                        if is_in_range(x_cood, anchors[i][0],anchors[i+1][0]):
                            index.append(i)
                            xs.append(x_cood)

            for j,i in enumerate(index):
                if i < self.num_of_anchor_in_up_curve - 1:
                    T = (xs[j] - min(old_anchors[i][0],old_anchors[i+1][0]))/(abs(old_anchors[i][0] - old_anchors[i+1][0]))
                    new_anchor_point = self.get_nth_curve(i)(T)
                    anchors = np.insert(anchors,i+a+1,new_anchor_point,axis = 0)
                    a += 1
                    num_of_up_anchors += 1
                else:
                    T = (max(old_anchors[i][0],old_anchors[i+1][0])-xs[j])/(abs(old_anchors[i][0] - old_anchors[i+1][0]))
                    new_anchor_point = self.get_nth_curve(i)(T)
                    anchors = np.insert(anchors,i+a+1,new_anchor_point,axis = 0)
                    num_of_bot_anchors += 1

        self.num_of_anchor_in_up_curve = num_of_up_anchors
        self.num_of_anchor_in_bottom_curve = num_of_bot_anchors
        return anchors

    def reset_points_by_anchors(self,anchors):
        # the num_of_up and bot anchors must fit:
        if not (self.num_of_anchor_in_bottom_curve+self.num_of_anchor_in_up_curve) == len(anchors):
            raise(Exception("number of anchors must fit the attribute: num_of_anchor_in_bottom_curve & num_of_anchor_in_up_curve"))
        #set up the up curve points:
        self.num_of_up_points =  3 * self.num_of_anchor_in_up_curve - 2 
        up_curve_points = np.zeros((self.num_of_up_points,self.dim))
        h1, h2 = get_smooth_handle_points(anchors[0:self.num_of_anchor_in_up_curve])# get smooth handles points
        up_curve_points[0] = anchors[0]
        arrays = [h1, h2, anchors[1:self.num_of_anchor_in_up_curve]]

        for index, array in enumerate(arrays):
            up_curve_points[index + 1::3] = array

        #set up the bot curve points:
        if self.set_up_the_bot_curve:
            self.number_of_bot_points = 3 *self.num_of_anchor_in_bottom_curve  # +1多添加了一个点
            bot_curve_points = np.zeros((self.number_of_bot_points,self.dim))

            h1, h2 = get_smooth_handle_points(anchors[self.num_of_anchor_in_up_curve-1:])
            arrays = [h2, h1, anchors[self.num_of_anchor_in_up_curve:]]
            for index, array in enumerate(arrays):
                bot_curve_points[index + 0::3] = array

            #integrate whole points
            self.points = np.append(up_curve_points,bot_curve_points, axis = 0)
        else:
            self.number_of_bot_points = 0
            self.points = up_curve_points

    def fit_to_new_axes(self,axes, is_logscaled_xaxis = False, old_axes = Axes()):
        # the distribution is set to the screen default xaxis
        # TODO: did not consider axes rotation

        # set the origin to the zero point on x_axis, not on y_axis
        new_origin = axes.x_axis.number_to_point(0)
        old_origin = old_axes.x_axis.number_to_point(0)

        new_x_unit_lenth = get_norm(new_origin - axes.x_axis.number_to_point(1))
        new_y_unit_lenth = get_norm(
            axes.y_axis.number_to_point(0) - axes.y_axis.number_to_point(1)
            )

        old_x_unit_lenth = get_norm(old_origin - old_axes.x_axis.number_to_point(1))
        old_y_unit_lenth = get_norm(
            old_axes.y_axis.number_to_point(0) - old_axes.y_axis.number_to_point(1)
            )

        # calculate the unit distance in new x_axis 
        x_strech_factor = np.divide(new_x_unit_lenth,old_x_unit_lenth)

        # zero point of y_axis might be different from zero point in x_axis
        y_strech_factor = np.divide(new_y_unit_lenth,old_y_unit_lenth)

        #shift and stretch about the new_origin
        self.points[:,0] = x_strech_factor*self.points[:,0]
        self.points[:,1] = y_strech_factor*self.points[:,1]
        self.shift(new_origin - old_origin)

        anchors = self.get_up_curve_anchors()
        self.mean = self.mean*x_strech_factor
        x_shift = self.mean - self.get_mean_point()[0]
        self.x_min = anchors[0][0] + x_shift
        self.x_max = anchors[-1][0] + x_shift

    def stack_over(self,distribution2):
        #stack self on top of distribution 2:
        #notice: the two distributions must be in the same coordinate system
        #if not, try fit_to_new_axes() first

        #move all 2 distribution to where it was on the ORIGINAL x_axis:
        shift_vec_self = np.array([self.mean,0,0]) - self.get_mean_point()
        shift_vec_distribution2 = np.array([distribution2.mean,0,0]) - distribution2.get_mean_point()
        self.shift(shift_vec_self)
        distribution2.shift(shift_vec_distribution2)
        
        if isinstance(distribution2,NormalDistribution):
            is_overlap, overlap_range = is_over_lap(
                self.x_min,
                self.x_max,
                distribution2.x_min,
                distribution2.x_max
                )

            if is_overlap:
                self.stack_mode = True
                new_anchors = self.get_anchors()
                dis2_anchors = distribution2.get_anchors()
                
                # add edge point as new anchor point 
                new_anchors_x = copy.deepcopy(overlap_range)
                #deepcopy so that any change in new_anchors_x would not affect overlap_range

                #change attributes .highest_points
                self.highest_points = np.array([self.highest_points,distribution2.highest_points])

                # add all the anchors of distribution2 within overlap range
                for point in dis2_anchors:
                    if is_in_range(point[0],overlap_range[0],overlap_range[1]) and not point[0] in new_anchors_x:
                        new_anchors_x.append(point[0])

                new_anchors = self.insert_new_anchor_by_x(new_anchors_x,new_anchors,multiple_xs = True)

                # raise the new anchor:
                for i,anchor in enumerate(new_anchors):
                    # if anchor point is within the overlap range
                    if is_in_range(anchor[0],overlap_range[0],overlap_range[1],include_edge = True):

                        anchor[1] += distribution2.get_distribution_value_by_x(anchor[0])

                # reset the whole curve
                self.reset_points_by_anchors(new_anchors)
                self.shift(-shift_vec_distribution2)
                distribution2.shift(-shift_vec_distribution2)               


#Group for Normal distribution, specifically the ones that were stacked together
class NDGroup(NormalDistribution):
    CONFIG = {
        }

    def __init__(self, *args, **kwargs):
        if len(args) == 1 and isinstance(args[0], (tuple, list)):
            args = args[0]

        #translate the distributions input arguments into packed_args list
        #note that the first argument must be the distribution in the bottom
        packed_args = []
        for arg in args:
            if isinstance(arg, (tuple, list)):
                packed_args.append(VGroup(arg))
            else:
                packed_args.append(arg)

        self.subdistributions = packed_args
        NormalDistribution.__init__(self,**kwargs)
        self.boundary_anchors = self.get_boundary_anchors()
        self.reset_points_by_anchors(self.boundary_anchors)


    def get_boundary_anchors(self):

        #set the x min and max to the bottom distribution
        dis_list = self.subdistributions
        x_min = dis_list[0].points[0][0]
        x_max = dis_list[0].get_up_curve_anchors()[-1][0]

        #reverse the distribution sequence so that the top is the first one
        dis_list.reverse()
        #from top to bot distributions
        for i,dis in enumerate(dis_list):

            #adjust the x max and min
            if x_min > dis.points[0][0]:
                x_min = dis.points[0][0]
            if x_max < dis.get_up_curve_anchors()[-1][0]:
                x_max = dis.get_up_curve_anchors()[-1][0]

            #from top to bottom, set the boundary anchors
            if i == 0:
                up_curve_anchors = dis.get_up_curve_anchors()
                up_max_x = dis.get_up_curve_anchors()[-1][0]
                up_min_x = dis.points[0][0]
                highest_points = dis.highest_points

                #self.highest_points = np.array([self.highest_points,distribution2.highest_points])

            else:
                for anchor in dis.get_up_curve_anchors():
                    #如果anchor的x值不在已填入范围的x内
                    if not is_in_range(anchor[0],up_min_x,up_max_x, include_edge = True):
                        #up_curve_anchors在最后加入anchor(最后再按照x大小排序)
                        up_curve_anchors = np.insert(up_curve_anchors,len(up_curve_anchors),anchor,axis = 0)

                if up_max_x < dis.x_max:
                    up_max_x = dis.x_max
                if up_min_x > dis.x_min:
                    up_min_x = dis.x_min

                #highest_points = np.insert(highest_points,len(highest_points),dis.highest_points,axis = 0)

        num_of_anchor_in_up_curve = len(up_curve_anchors)
        #recover the distribution sequence from bot to top
        dis_list.reverse()
        self.num_of_anchor_in_up_curve = len(up_curve_anchors)
        up_curve_anchors = sort_points_by_x(up_curve_anchors)

        self.x_max = x_max
        self.x_min = x_min
        self.mean = np.divide(x_max+x_min,2)
        
        return up_curve_anchors
