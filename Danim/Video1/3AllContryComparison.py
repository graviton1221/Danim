from Danim.Contry import *

#坐标轴设置axes settings
population_per_circle_area = 1/1.4*1.2 # default: 1.4 billion people is a 1.2unit area circle
xmin = 0
xmax = 100
ymin = 0
ymax = 10
proportion_to_left = 0.9 #default x axis move to 10% empty space left, note its the proportion to the origin
proportion_to_bottom = 0.8
x_scale_factor = (proportion_to_left+1)*FRAME_X_RADIUS/(xmax-xmin)*0.96 # 0.96 is arrow buff
y_scale_factor = (proportion_to_bottom+1)*FRAME_Y_RADIUS/(ymax-ymin)*0.96
NEWORIGIN = [-FRAME_X_RADIUS*proportion_to_left,-FRAME_Y_RADIUS*proportion_to_bottom,0]

mode = "chinese"

class AllContryComparison(Scene):

    def construct(self, mode = mode):
        #logotag
        logotag = TextMobject("引力子G @B站").scale(0.4)
        logotag.to_edge(DR)
        logotag.shift(0.4*DOWN+0.4*RIGHT)
        logotag.asdfi = 1# no use, for not fadeout in the end
        self.add(logotag)
        self.wait(1)
        
        #--------------------------------创建坐标系
        axes = Axes(
            x_min = xmin,
            x_max = xmax,
            y_min = ymin,
            y_max = ymax,
            x_tick_frequency = 10,
            x_axis_config = {"tick_frequency":10,"leftmost_tick": 10,},
            y_axis_config = {"label_direction":LEFT},
            )
        axes.x_axis.move_to(ORIGIN,aligned_edge=LEFT)
        axes.y_axis.move_to(ORIGIN,aligned_edge=DOWN)
        axes.x_axis.stretch_about_point(x_scale_factor, 0, ORIGIN)
        axes.y_axis.stretch_about_point(y_scale_factor, 1, ORIGIN)
        axes.shift(NEWORIGIN)
        
        
        for number in range(10,100,10):
            axes.x_axis.add_numbers(number)
        for number in range(1,10):
            axes.y_axis.add_numbers(number)        
        
        self.play(ShowCreation(axes),run_time = 1.5)


        y_axis_label_text = TextMobject("生育率").scale(0.6)
        y_axis_label_text.next_to(axes.y_axis.number_to_point(9), RIGHT+UP)

        x_axis_label_text = TextMobject("人均寿命").scale(0.6)
        x_axis_label_text.next_to(axes.x_axis.number_to_point(95), UP)
        self.play(Write(y_axis_label_text),Write(x_axis_label_text),run_time = 1)

        #create year lable:
        year_lable = Integer(1800,group_with_commas = False,color = TEAL_E).scale(1.5)
        year_lable.to_edge(UR)
        self.play(GrowFromCenter(year_lable),run_time =0.6)
        
        #create add all areas circles
        area_rect = []
        area_rect_lable = []
        areas = []
        for i,area in enumerate(THE_WHOLE_WORLD):

            areas.append(Area(area,show_CN_name = True))
            area_rect.append(Rectangle(height = 0.2, width = 0.5,color = AREA_COLOR_MAP[i],fill_opacity = 1))
            
            if i == 0:
                area_rect[i].next_to(year_lable,2*DOWN)

            else:
                area_rect[i].next_to(area_rect[i-1],DOWN)
            area_rect_lable.append(TextMobject(CH_THE_WHOLE_WORLD[i]).scale(0.4))
            area_rect_lable[i].next_to(area_rect[i],LEFT)

            areas[i].generate_all_contry_circles(
                years_date=1800,
                COLORMAT = [AREA_COLOR_MAP[i]],
                if_switch_on =True,
                Axes = axes,
                sort_by_axes =True
                )
            self.play(*areas[i].get_creation_animation(sort_by_axes= True),
                GrowFromCenter(area_rect[i]),
                Write(area_rect_lable[i])
                )
            self.wait(2)
            self.play(AnimationGroup(*areas[i].transform_animations,lag_ratio = 0.1))

        
        #update the contry circles from 1800 - 1911
        TIME_TOTOL = 30

        transfer_time = 0.7*TIME_TOTOL/len(range(1801,1911,1))
        wait_time = 0.3*TIME_TOTOL/len(range(1801,1911,1))

        for new_year in range(1801,1911,1):
            area_animation = []
            contry_name_anim = []
            for area in areas:
                area_animation += area.update_area_contryname_by_year_animation(new_year)
                area_animation += area.update_area_circles_by_year_animation(new_year)
                # SEQUENCE matters
                    
            self.play(
                *area_animation,
                year_lable.set_value,new_year,
                run_time = transfer_time
                )
            self.wait(wait_time)


        #update the contry circles from 1911 - 1923 :WW1
        self.wait()

        TIME_TOTOL = 30

        transfer_time = 0.7*TIME_TOTOL/len(range(1911,1923,1))
        wait_time = 0.3*TIME_TOTOL/len(range(1911,1923,1))

        for new_year in range(1911,1923,1):
            area_animation = []
            contry_name_anim = []
            for area in areas:
                area_animation += area.update_area_contryname_by_year_animation(new_year)
                area_animation += area.update_area_circles_by_year_animation(new_year)
                # SEQUENCE matters
            
            self.play(
                *area_animation,
                year_lable.set_value,new_year,
                run_time = transfer_time
                )
            self.wait(wait_time)

        self.wait()

        #update the contry circles from 1920 - 1950 :WW2
        TIME_TOTOL = 30

        transfer_time = 0.7*TIME_TOTOL/len(range(1923,1950,1))
        wait_time = 0.3*TIME_TOTOL/len(range(1923,1950,1))

        for new_year in range(1923,1950,1):
            area_animation = []
            contry_name_anim = []
            for area in areas:
                area_animation += area.update_area_contryname_by_year_animation(new_year)
                area_animation += area.update_area_circles_by_year_animation(new_year)
                # SEQUENCE matters
            
            self.play(
                *area_animation,
                year_lable.set_value,new_year,
                run_time = transfer_time
                )
            self.wait(wait_time)

        self.wait()

        #update the contry circles from 1950 - 2018:

        TIME_TOTOL = 30

        transfer_time = 0.7*TIME_TOTOL/len(range(1951,2019,1))
        wait_time = 0.3*TIME_TOTOL/len(range(1951,2019,1))

        for new_year in range(1951,2018,1):
            area_animation = []
            contry_name_anim = []
            for area in areas:
                area_animation += area.update_area_contryname_by_year_animation(new_year)
                area_animation += area.update_area_circles_by_year_animation(new_year)
                # SEQUENCE matters
            
            self.play(
                *area_animation,
                year_lable.set_value,new_year,
                run_time = transfer_time
                )
            self.wait(wait_time)

        self.wait()



        animations = []
        for mob in self.mobjects:
            if isinstance(mob,Mobject) & (not hasattr(mob,"asdfi")):
                animations.append(FadeOut(mob))

        self.play(*animations)
        
