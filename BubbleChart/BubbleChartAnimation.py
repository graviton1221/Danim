#added functions
from Danim.BubbleChart.BubbleChart import *

class BubbleChartAnimation(Scene):
    def construct(self):
        self.AllContriesComparison()
        #self.TwoContriesComparison()


    def AllContriesComparison(
        self,
        start_option = "2"
        ):
        #data import:
        X,Y,R,entity_names,T = data_digest()

        #creation_ animation has three option： 
        #option 1: directly create everything
        #option 2: create bubble one by one(color randomly)
        #option 3: create bubble one by one(sort by color group)

        
        #option 1: start-----------------------------------------------------------------
        if start_option == "1":
            #create bubble_chart object
            bubble_chart = BubbleChart(X,Y,R,entity_names,T,axis_color = RED, set_bubble_colors = "by_group")

            #make Creation animation
            self.play(bubble_chart.Get_Creation_Animation())
            self.wait()
        #option 1: end-------------------------------------------------------------------
        

        #option 2: start-----------------------------------------------------------------
        if start_option == "2":

            bubble_chart = BubbleChart(X,Y,R,entity_names,T,axis_color = RED, set_bubble_colors = "randomly",show_creation = True)
            
            bubble_chart.Get_Creation_Animation(
                directly_show_creation = False,
                initial_position = 4*RIGHT+3*UP,
                maximum_circles_to_show = NUM_OF_MAXIMUM_CIRCLES_IN_A_FRAME
                )

            self.play(ShowCreation(VGroup(bubble_chart.axes,bubble_chart.lables)))
            quotient = len(bubble_chart.entity_names)//NUM_OF_MAXIMUM_CIRCLES_IN_A_FRAME
            remainder = len(bubble_chart.entity_names)%NUM_OF_MAXIMUM_CIRCLES_IN_A_FRAME

            for i in range(quotient):
                
                self.play(
                    *bubble_chart.grow_animation[NUM_OF_MAXIMUM_CIRCLES_IN_A_FRAME*i:NUM_OF_MAXIMUM_CIRCLES_IN_A_FRAME*(i+1)],
                    lag_ratio = LAG_RATIO_FOR_CREATION
                    )

                self.wait()
                self.play(
                    AnimationGroup(*bubble_chart.transfer_animation[NUM_OF_MAXIMUM_CIRCLES_IN_A_FRAME*i:NUM_OF_MAXIMUM_CIRCLES_IN_A_FRAME*(i+1)],
                    lag_ratio = LAG_RATIO_FOR_CREATION)
                    )

            self.wait()

            self.play(
                AnimationGroup(*bubble_chart.grow_animation[NUM_OF_MAXIMUM_CIRCLES_IN_A_FRAME*(quotient):len(bubble_chart.entity_names)],
                lag_ratio = LAG_RATIO_FOR_CREATION)
                )
            self.wait()
            self.play(AnimationGroup(*bubble_chart.transfer_animation[NUM_OF_MAXIMUM_CIRCLES_IN_A_FRAME*(quotient):len(bubble_chart.entity_names)],
                lag_ratio = LAG_RATIO_FOR_CREATION)
                )

            self.wait()
        #option 2: end-------------------------------------------------------------------

        #option 3: start-----------------------------------------------------------------
        if start_option == "3":
            bubble_chart = BubbleChart(X,Y,R,entity_names,T,axis_color = RED, set_bubble_colors = "by_group",show_creation = True)
            
            bubble_chart.Get_Creation_Animation(
                directly_show_creation = False,
                initial_position = 3*RIGHT+3*UP,
                maximum_circles_to_show = NUM_OF_MAXIMUM_CIRCLES_IN_A_FRAME
                )

            self.play(ShowCreation(VGroup(bubble_chart.axes,bubble_chart.lables)))
            quotient = len(bubble_chart.entity_names)//NUM_OF_MAXIMUM_CIRCLES_IN_A_FRAME
            remainder = len(bubble_chart.entity_names)%NUM_OF_MAXIMUM_CIRCLES_IN_A_FRAME

            index_track = 0
            for i,name in enumerate(SHOWN_ENTITY_NAMES):

                self.play(bubble_chart.color_lables_animation[i])

                num_of_subentities = len(bubble_chart.indices[i])
                self.play(
                    AnimationGroup(
                        *bubble_chart.grow_animation[index_track:num_of_subentities+index_track],
                        lag_ratio = LAG_RATIO_FOR_CREATION))
                self.wait()

                
                self.play(
                    AnimationGroup(
                        *bubble_chart.transfer_animation[index_track:num_of_subentities+index_track],
                        lag_ratio = LAG_RATIO_FOR_CREATION
                        )
                    )

                self.wait()

                index_track = index_track + num_of_subentities

            bubble_chart.lables.add(bubble_chart.color_lables)

            self.wait()
        #option 3: end-------------------------------------------------------------------

        
        #set the whole animation run time
        num_of_iterations = len(range(len(bubble_chart.times)-1))
        if SET_BY_TOTAL_TIME:
            bubble_time = BUBBLE_TRANSFROMATION_RUN_TIME/num_of_iterations
            lable_time = TIME_LABLE_TRANSFROMATION_RUN_TIME/num_of_iterations
            wait_time = WAIT_TIME/num_of_iterations

        #Update the whole animations:           
        for year in range(len(bubble_chart.times)-1):
            print(bubble_chart.times[year])
            self.play(
                *bubble_chart.Time_Update_Animation(
                    year+1,
                    bubble_transform_time = bubble_time,
                    time_lable_run_time = lable_time
                    )
                )
        
        
        #this is the hight_light animation code
        #use when needed
        '''
        animations = bubble_chart.Get_Hightlight_Animation(
                ["China","India","Japan","Russia","United States"],
                wait_time = [1,2,1,2,1],
                intersection_wait_time = 1,
                directions = [DOWN,DOWN,UP,2*DOWN,2*UP],
                current_time_index = bubble_chart.get_current_timeindex(),
                fadeout_at_once = True
                )

        for anim in animations:
            if isinstance(anim,list):
                self.play(*anim)
            else:
                self.play(anim)
        '''

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

