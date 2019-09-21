from manimlib.imports import *

from Danim.BubbleChart.BCutils import *
from Danim.BubbleChart.bubble_constants import *

class BubbleChart(VGroup):
    # A class to quickly create the bubble chart animation  
    # may not have the freedom to change things

    CONFIG = {
    "show_axes_lable": SHOW_AXIS_LABLES, #default True
    "show_time_lable": True, # names to show are stored in SHOWN_ENTITY_NAMES
    "show_color_lables": True, # default group names
    "set_bubble_colors": "randomly",# two options: "by_group" or "randomly"
    "x_axis_lable": X_AXIS_LABLE,
    "y_axis_lable": Y_AXIS_LABLE,
    "show_creation": False
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
           
        if not self.show_creation:
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
        else:
            self.lables_creation()
            VGroup.__init__(self, **kwargs)
            self.add(
                self.axes,
                self.lables
                )
            #the bubbles and will be created later
            #using animation method self.Get_Creation_Animation(directly_show_creation = False)

    def get_current_timeindex(self):
        return self.times.index(self.time_lable.get_tex_string())



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

            #read information from "Group_lable.csv"
            group_lable_data = np.array(
                pd.DataFrame(
                    pd.read_csv(GROUP_LABLE_CSV_FILE, encoding = "gbk", index_col = 0),
                    index = self.entity_names
                    )
                )
            
            #check whether the numbers of rows are the same
            assert(len(COLORMAT) == group_lable_data.shape[0])

            self.group_index = []
            #match color to COLORMAT with relationship in COLOR_LABLE_DICT
            for i,lable in enumerate(group_lable_data):
                if lable[0] in COLOR_LABLE_DICT:
                    COLORMAT[i] = COLOR_LABLE_DICT[lable[0]]
                    self.group_index.append(COLOR_LABLE_INDEX_DICT[lable[0]])

        #generate color randomly
        elif self.set_bubble_colors == "randomly":
            COLORMAT = []
            for i in range(0,self.coordinates.shape[0]+1):
                COLORMAT.append(random_color())


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

            #self.lables.add(self.time_lable)

        #create color lables(with rectangles)
        if self.show_color_lables and (not self.show_creation):

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


    def Get_Creation_Animation(
        self,
        directly_show_creation = True, 
        maximum_circles_to_show = 50,
        creation_time_index = 0,
        initial_position = 3*UP + 3*RIGHT
        ):

        creation_time = self.times[creation_time_index]

        #Show Creation all together
        if directly_show_creation:
            self.lables_creation()
            #self.add(self.lables)
            return ShowCreation(self,run_time = CREATION_RUN_TIME)

        #Show creaton with all name listed
        else:

            self.color_lables = VGroup()
            old_bubbles = []
            transfered_bubbles = []
            name_lables = []
            self.circle_index = []
            self.bubbles = VGroup()
            self.grow_animation = []
            self.transfer_animation = []
            self.color_lables_animation = []
            

            def generate_circle_matrix(indices):
                #indices is the relative index 
                #position in self.entity_names

                new_entity = []
                y0 = self.axes.x_axis.number_to_point(self.axes.x_axis.x_max)[1]

                for i,name in enumerate(self.entity_names):
                    if i in indices:
                        new_entity.append(name)

                if not len(old_bubbles) == 0:
                    start_index = len(old_bubbles)
                else:
                    start_index = 0

                for j,name in enumerate(new_entity):

                    #old_bubble creation
                    if j == 0:
                        previous_index = start_index
                        cornor_index = start_index

                        old_bubbles.append(
                            set_up_the_bubbles(
                                initial_position, 
                                self.radiusdata[indices[j],creation_time_index], 
                                self.axes, 
                                self.COLORMAT[indices[j]],
                                mode = 'single'
                                )
                            )

                    else:
                        old_bubbles.append(
                            set_up_the_bubbles(
                                np.array([0,0,0]), 
                                self.radiusdata[indices[j],creation_time_index], 
                                self.axes, 
                                self.COLORMAT[indices[j]],
                                mode = 'single'
                                )
                            )


                    #name_lable creation
                    if SHOW_CN_NAMES:
                        name_shown = online_translation(name)
                    else:
                        name_shown = name

                    name_lables.append(
                        TextMobject(
                            name_shown
                            ).scale(
                                NAME_TEXT_SCALE_FACTOR
                                )
                            )

                    name_lables[-1].next_to(old_bubbles[-1],RIGHT)

                    #check if circle matrix reaches the bottom
                    height = old_bubbles[-1].get_critical_point(UP)[1] - old_bubbles[-1].get_critical_point(DOWN)[1]
                    cell = old_bubbles[previous_index].get_critical_point(DOWN)[1]

                    if not j == 0:
                        current_VGroup = VGroup(old_bubbles[-1],name_lables[-1])
                        # if the curreny circle touches the bottom:
                        if cell - height < y0 + 0.5:                            
                            current_VGroup.next_to(old_bubbles[cornor_index],LEFT)
                            current_VGroup.shift(0.25*LEFT)
                            cornor_index = len(old_bubbles) - 1
                        # if the curreny circle does not touch the bottom:
                        else:
                            current_VGroup.next_to(previous_VGroup,DOWN)
                                      
                    #transfered_bubbles creation:
                    transfered_bubbles.append(
                        set_up_the_bubbles(
                            self.coordinates[indices[j],creation_time_index], 
                            self.radiusdata[indices[j],creation_time_index], 
                            self.axes, 
                            self.COLORMAT[indices[j]],
                            mode = 'single'
                            )
                        )

                    #record the circle index
                    self.circle_index.append(indices[j])

                    #append the animation
                    self.grow_animation.append(
                        AnimationGroup(
                            FadeIn(
                                old_bubbles[-1]                                    
                                ),
                            Write(
                                name_lables[-1]
                                ),
                            run_time = SINGLE_GROW_RUN_TIME
                            )
                        )

                    self.transfer_animation.append(
                        AnimationGroup(
                            ReplacementTransform(
                                old_bubbles[-1],
                                transfered_bubbles[-1]
                                ),
                            FadeOut(
                                name_lables[-1]),
                            run_time = SINGLE_TRANSFER_TIME
                            )

                        )

                    previous_index = len(old_bubbles) - 1
                    previous_VGroup = VGroup(old_bubbles[-1],name_lables[-1])


            if self.set_bubble_colors == "randomly":
                indices = []
                for i,name in enumerate(self.entity_names):
                    indices.append(i)

                quotient = len(self.entity_names)//maximum_circles_to_show
                remainder = len(self.entity_names)%maximum_circles_to_show
                    
                for i in range(quotient):
                    generate_circle_matrix(indices[maximum_circles_to_show*(i):maximum_circles_to_show*(i+1)])


                #generate_circle_matrix(indices[maximum_circles_to_show*(i+1):len(self.entity_names)])

                self.bubbles = VGroup(*transfered_bubbles)

            #if set bubbles by group 
            #usurally with self.show_color_lables = True:
            else:
                if self.show_color_lables:

                    entity_color_map = dict(
                        dict(zip(self.entity_names,self.COLORMAT)),
                        **COLOR_LABLE_DICT
                        )

                self.indices = []
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

                        self.color_lables_animation.append(
                            AnimationGroup(
                                FadeIn(rect),
                                Write(rect_name)
                                )
                            )

                        self.color_lables.add(rect,rect_name)

                        indice = []
                        for j,name in enumerate(self.entity_names):
                            if self.COLORMAT[j] == COLOR_LABLE_DICT[entity]:
                                indice.append(j)
                        
                        generate_circle_matrix(indice)
                        self.indices.append(indice)

                def sort_by_index(listA,index_list):
                    assert(len(listA) == len(index_list))
                    new_list = []
                    for z,element in enumerate(listA):
                        new_list.append(listA[index_list[z]])

                    return new_list


                index_list = []
                for indice in self.indices:
                    index_list = index_list + indice
                new_bubbles = sort_by_index(transfered_bubbles,index_list)
                #self.bubbles = VGroup()
                for bubble in new_bubbles:
                    self.bubbles.add(bubble)

            #self.lables.add(self.color_lables)
            self.add(self.bubbles)

            #sort the animation by data index
            #originally theanimation list is sort by creation order

    def Get_Hightlight_Animation(
        self,
        names_to_show,#list of str, must be elements in self.entity_names
        wait_time = None,#a number or list of numbers, lens must match the number of entities
        intersection_wait_time = 1, 
        directions = None, 
        #directions is a list of direction vectors, 
        #lens must match the number of entities, 
        #if none, lables will choose
        lable_sizes = None,
        #lable_sizes is a list of numbers indicating the size of each lable
        #lens must match the number of entities to show
        wiggle_time = None,
        wiggle_factor = None,
        fadeout_time = None,
        current_time_index = 0,
        fadeout_at_once = False#
        ):
        
        if isinstance(names_to_show,list):
            numbers_of_entities = len(names_to_show)
        else:
            numbers_of_entities = 1

        if directions is None:
            directions = [UP]*numbers_of_entities
        
        if wiggle_factor is None:
            wiggle_factor = [1.5]*numbers_of_entities
        
        if wiggle_time is None:
            wiggle_time = [1.5]*numbers_of_entities

        if lable_sizes is None:
            lable_sizes = [0.7]*numbers_of_entities

        if fadeout_time is None:
            fadeout_time = [1]*numbers_of_entities

        if wait_time is None:
            wait_time = [1]*numbers_of_entities

        old_lables = []
        new_lables = []
        indices = []
        animation = []


        #TODO: add empty animation more efficiently
        #Currently I add empty animation the dumb way! 
        #add a black dot outside the screen!
        #I don't know how to add empty
        dumb_dot = Dot(color = BLACK).shift(100*UR)


        intersection_wait_animation = ApplyMethod(
            dumb_dot.shift,
            0.1*RIGHT,
            run_time = intersection_wait_time
            )
        
        for i,name in enumerate(names_to_show):
            if name in self.entity_names:
                
                indices.append(self.entity_names.index(name))

                if SHOW_CN_NAMES:
                    name_to_show = online_translation(name)
                else:
                    name_to_show = name

                mid_wait_animation = ApplyMethod(
                    dumb_dot.shift,
                    0.1*RIGHT,
                    run_time = wait_time[i]
                    )
                
                old_lables.append(
                    TextMobject(
                        name_to_show,
                        color = self.COLORMAT[indices[i]]
                        ).scale(0.1)
                    )

                new_lables.append(
                    TextMobject(
                        name_to_show,
                        color = self.COLORMAT[indices[i]]
                        ).scale(lable_sizes[i])
                    )

                old_lables[i].move_to(
                    self.coordinates[indices[i],current_time_index]
                    )

                new_lables[i].next_to(
                    self.bubbles.submobjects[indices[i]],
                    directions[i]
                    )
                
                animation.append(
                    ShowCreation(old_lables[i],run_time = 0.02)
                    )
                '''
                animation.append(
                    AnimationGroup(
                        ReplacementTransform(
                            old_lables[i],
                            new_lables[i],
                            run_time = wiggle_time[i]
                            ),
                        WiggleOutThenIn(
                            self.bubbles.submobjects[indices[i]],
                            scale_value = wiggle_factor[i],
                            run_time = wiggle_time[i]
                            )
                        )
                    )
                '''
                animation.append(
                    [ReplacementTransform(
                        old_lables[i],
                        new_lables[i],
                        run_time = wiggle_time[i]
                        ),
                    WiggleOutThenIn(
                        self.bubbles.submobjects[indices[i]],
                        scale_value = wiggle_factor[i],
                        run_time = wiggle_time[i]
                        )]
                    )

                animation.append(mid_wait_animation)
                if not fadeout_at_once:
                    animation.append(
                        FadeOut(
                            new_lables[i],
                            run_time = fadeout_time[i]
                            )
                        )

                animation.append(intersection_wait_animation)

        if fadeout_at_once:
            lables = VGroup()
            for lable in new_lables:
                lables.add(lable)
                print(len(lables.submobjects))
            animation.append(FadeOut(lables,run_time = fadeout_time[0]))
        print(len(animation))

        return animation

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
        new_circles = VGroup()

        for i,bubbledata in enumerate(zip(self.coordinates[:,t],self.radiusdata[:,t])):
            
            new_circle = Circle(
                radius = bubbledata[1],
                color = self.COLORMAT[i], 
                fill_opacity = FILL_OPACITY).shift(bubbledata[0]
                )
            
            new_circles.add(new_circle)

        new_circles, self.bubbles = self.bubbles,new_circles
        if not show_track:
            args.append(
                ReplacementTransform(
                    new_circles,
                    self.bubbles,
                    run_time = bubble_transform_time                    
                    )
                )

        else:
            args.append(
                Transform(
                    new_circles,
                    self.bubbles,
                    run_time = bubble_transform_time                    
                    )
                )
            '''

            #new_circle,self.bubbles.submobjects[i] = self.bubbles.submobjects[i],new_circle
            
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
            '''

        # update the time lable:
        if hasattr(self,"time_lable"):
            
            new_time_lable = (TextMobject(
                str(self.times[t]),
                color = TIME_LABLE_COLOR).scale(
                    TIME_LABLE_SCALE_FACTOR
                    )
                ).shift(TIME_LABLE_POSITION)

            new_time_lable,self.time_lable = self.time_lable,new_time_lable

            args.append(
                ReplacementTransform(
                    new_time_lable,
                    self.time_lable,
                    run_time = time_lable_run_time)
                )

        return args
