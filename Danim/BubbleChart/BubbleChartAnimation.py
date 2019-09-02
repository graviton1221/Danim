#mainm tools
from manimlib.imports import *
#added functions
from Danim.BubbleChart.BCutils import *
from Danim.BubbleChart.bubble_constants import *


class BubbleChartAnimation(Scene):
    def construct(self):
        self.AllContriesComparison()
        #self.TwoContriesComparison()

    def AllContriesComparison(self):
        #data import:
        X,Y,R,entity_names,T = data_digest()
        #create bubble_chart object
        bubble_chart = BubbleChart(X,Y,R,entity_names,T,axis_color = RED, set_bubble_colors = "by_group")

        #make Creation animation
        self.play(bubble_chart.Get_Creation_Animation())
        self.wait()
        
        
        #set the whole animation run time
        num_of_iterations = len(range(len(bubble_chart.times)-1))
        if SET_BY_TOTAL_TIME:
            bubble_time = BUBBLE_TRANSFROMATION_RUN_TIME/num_of_iterations
            lable_time = TIME_LABLE_TRANSFROMATION_RUN_TIME/num_of_iterations
            wait_time = WAIT_TIME/num_of_iterations
        
        #Update the whole animations:           
        for year in range(len(bubble_chart.times)-1):
            self.play(
                *bubble_chart.Time_Update_Animation(
                    year+1,
                    bubble_transform_time = bubble_time,
                    time_lable_run_time = lable_time
                    )
                )

            self.wait(wait_time)
        
        #TODO: FadeOut Everything
        

    def TwoContriesComparison(self):
        #data import:
        X,Y,R,entity_names,T = data_digest(display_specific_entities = True,entity_name_list = ["Vietnam","United States"])
        
        #create bubble_chart object
        bubble_chart = BubbleChart(X,Y,R,entity_names,T,axis_color = RED, set_bubble_colors = "randomly")

        self.play(ShowCreation(bubble_chart))

        #set the whole animation run time
        num_of_iterations = len(range(0,len(bubble_chart.times)-1,3))
        if SET_BY_TOTAL_TIME:
            bubble_time = BUBBLE_TRANSFROMATION_RUN_TIME/num_of_iterations
            lable_time = TIME_LABLE_TRANSFROMATION_RUN_TIME/num_of_iterations
            wait_time = WAIT_TIME/num_of_iterations

        print(bubble_time,lable_time,wait_time)
        
        #Update the whole animations:           
        for year in range(0,len(bubble_chart.times)-1,3):
            self.play(
                *bubble_chart.Time_Update_Animation(
                    year+1,
                    bubble_transform_time = bubble_time,
                    time_lable_run_time = lable_time,
                    show_track = True
                    )
                )

            self.wait(wait_time)



class BubbleChart(VGroup):
    # A class to quickly create the bubble chart animation, 
    # may not have the freedom to change things

    CONFIG = {
    "show_axes_lable": SHOW_AXIS_LABLES, #default True
    "show_time_lable": True, # names to show are stored in SHOWN_ENTITY_NAMES
    "show_color_lables": True, # default group names
    "set_bubble_colors": "randomly",# two options: "by_group" or "randomly"
    "x_axis_lable": X_AXIS_LABLE,
    "y_axis_lable": Y_AXIS_LABLE,
    }


    def __init__(self, X, Y, R, entity_names, T, **kwargs):
        
        #CONFIG to attributes
        digest_config(self,kwargs)
        self.entity_names = entity_names
        self.times = T

        #create axes
        (self.axes_config,
            self.axes
            ) = import_data_and_set_axes(X,Y)
        
        #transform X,Y,R into screen coordinates
        self.coordinates,self.radiusdata = transform_from_data_to_screencoordinates(X,Y,R,self.axes)

        #set the colors of bubbles:
        #COLORMAT is a list of shape(num_of_bubbles,1)
        #each element is a color array
        self.COLORMAT = self.generate_colormatrix()

        #set the bubble to the start time
        self.bubbles = set_up_the_bubbles(
            self.coordinates[:,0],
            self.radiusdata[:,0],
            self.axes, 
            color_mat = self.COLORMAT
            )

        #create lables
        self.lables_creation()


        VGroup.__init__(self, **kwargs)
        self.add(
            self.axes,
            self.bubbles,
            self.lables
            )

    def generate_colormatrix(self, colors = None):

        # the color of each bubbles can be set by some group lables
        # for example: if each bubble represents a contry, then
        # you can set all the contry in Asia as red bubbles, 
        # North American Contries as blue bubbles
        # you need a cvs file called the "Group_lable.csv" to store each tags
        # or you can just put a dic to represents that relationship
        if self.set_bubble_colors == "by_group":
            #generate color matrices with default color red
            COLORMAT = [RED]*self.coordinates.shape[0]

            #red information from "Group_lable.csv"
            group_lable_data = np.array(
                pd.DataFrame(
                    pd.read_csv(GROUP_LABLE_CSV_FILE, encoding = "gbk", index_col = 0),
                    index = self.entity_names
                    )
                )
            
            #check whether the numbers of rows are the same
            assert(len(COLORMAT) == group_lable_data.shape[0])
            
            #match color to COLORMAT with relationship in COLOR_LABLE_DICT
            for i,lable in enumerate(group_lable_data):
                if lable[0] in COLOR_LABLE_DICT:
                    COLORMAT[i] = COLOR_LABLE_DICT[lable[0]]

        #generate color randomly
        elif self.set_bubble_colors == "randomly":
            COLORMAT = []
            for i in range(0,self.coordinates.shape[0]+1):
                COLORMAT.append(random_color())

            print(len(COLORMAT))

        else:
            COLORMAT = [RED*self.coordinates.shape[0]]

        



        return COLORMAT

    def lables_creation(self):
        #lable creation:
        self.lables = VGroup()

        if self.show_axes_lable:
            #Create the x_axis_lable
            self.lables.add(
                (TextMobject(
                    self.x_axis_lable, color = TEXT_COLOR
                    ).scale(
                        TEXT_SCALE_FACTOR
                        )
                    ).shift(
                        self.axes.x_axis.number_to_point(self.axes.x_axis.x_max) + X_LABLE_ADJUST_VECTOR
                        )
                    )

            #create the y_axis_lable:
            self.lables.add(
                (TextMobject(
                    self.y_axis_lable, color = TEXT_COLOR
                    ).scale(
                        TEXT_SCALE_FACTOR
                        )
                    ).shift(
                        self.axes.y_axis.number_to_point(self.axes.y_axis.x_max) + Y_LABLE_ADJUST_VECTOR
                        )
                    )

        #create the time lable
        if self.show_time_lable:
            self.time_lable = (TextMobject(
                str(self.times[0]),
                color = TIME_LABLE_COLOR).scale(
                    TIME_LABLE_SCALE_FACTOR
                    )).shift(TIME_LABLE_POSITION)

            self.lables.add(self.time_lable)

        #create color lables(with rectangles)
        if self.show_color_lables:

            entity_color_map = dict(
                dict(zip(self.entity_names,self.COLORMAT)),
                **COLOR_LABLE_DICT
                )

            self.color_lables = VGroup()
            for i,entity in enumerate(SHOWN_ENTITY_NAMES):
                if entity in entity_color_map:
                    rect = Rectangle(
                            height = RECT_HIGHT, 
                            width = RECT_WIDTH,
                            color = entity_color_map[entity],
                            fill_opacity = 1)

                    if SHOW_CN_NAMES:
                        name_to_show = online_translation(entity)
                        rect_name = TextMobject(name_to_show).scale(
                        RECT_TEXT_SCALE_FACTOR)
                    else:
                        rect_name = TextMobject(entity).scale(
                        RECT_TEXT_SCALE_FACTOR)
                    if i == 0:
                        rect.shift(RECT_POSITION)
                        rect_name.next_to(rect,RIGHT)
                    else:
                        rect.align_to(self.color_lables,direction = LEFT+DOWN)
                        rect.shift(DOWN* RECT_HIGHT*RECT_INTERVAL_FACTOR)
                        rect_name.next_to(rect,RIGHT)

                    self.color_lables.add(rect,rect_name)

            self.lables.add(self.color_lables)



    def Get_Creation_Animation(self):
        return ShowCreation(self,run_time = CREATION_RUN_TIME)

    def Time_Update_Animation(
        self,
        t, 
        bubble_transform_time = BUBBLE_TRANSFROMATION_RUN_TIME,
        time_lable_run_time = TIME_LABLE_TRANSFROMATION_RUN_TIME,
        show_track = False
        ):
        # to a specific time, t can be index(integer) within range(0,len(self.times+1))
        # or t can be a element in self.times

        args = []

        #if t is not a index, we need to convert it into index
        if not isinstance(t,int):
            if not t in self.times:
                raise Exception("input argument 't' is not in self.times")
            else:#if t is not a index, but is a element in self.times
                t = self.times.index(t)

        #update the bubbles
        for i,bubbledata in enumerate(zip(self.coordinates[:,t],self.radiusdata[:,t])):
            
            new_circle = Circle(
                radius = bubbledata[1],
                color = self.COLORMAT[i], 
                fill_opacity = FILL_OPACITY).shift(bubbledata[0]
                )
            new_circle,self.bubbles.submobjects[i] = self.bubbles.submobjects[i],new_circle

            if not show_track:
                args.append(
                    ReplacementTransform(
                        new_circle,
                        self.bubbles.submobjects[i],
                        run_time = bubble_transform_time                    
                        )
                    )
            else:
                args.append(
                    Transform(
                        new_circle,
                        self.bubbles.submobjects[i],
                        run_time = bubble_transform_time                    
                        )
                    )
        
        # update the time lable:
        if hasattr(self,"time_lable"):

            new_time_lable = (TextMobject(
                str(self.times[t]),
                color = TIME_LABLE_COLOR).scale(
                    TIME_LABLE_SCALE_FACTOR
                    )
                ).shift(TIME_LABLE_POSITION)

            self.time_lable,new_time_lable = new_time_lable,self.time_lable

            args.append(
                ReplacementTransform(
                    new_time_lable,
                    self.time_lable,
                    run_time = time_lable_run_time
                    )
                )

        return args
