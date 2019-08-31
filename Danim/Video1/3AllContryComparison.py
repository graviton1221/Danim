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
        
        self.play(ShowCreation(axes),run_time = 5)


        y_axis_label_text = TextMobject("生育率").scale(0.6)
        y_axis_label_text.next_to(axes.y_axis.number_to_point(9), RIGHT+UP)

        x_axis_label_text = TextMobject("人均寿命").scale(0.6)
        x_axis_label_text.next_to(axes.x_axis.number_to_point(95), UP)
        self.play(Write(y_axis_label_text),Write(x_axis_label_text),run_time = 1)

        #create year lable:
        year_lable = Integer(1800,group_with_commas = False,color = TEAL_E).scale(1.5)
        year_lable.to_edge(UR)
        self.play(GrowFromCenter(year_lable),run_time =3)
        
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
        TIME_TOTOL = 30 # 3.76 years per sec

        transfer_time = 0.7*TIME_TOTOL/len(range(1801,1913,1))
        wait_time = 0.3*TIME_TOTOL/len(range(1801,1913,1))

        for new_year in range(1801,1913,1):
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

        TIME_TOTOL = 20 # 1.88 years per sec

        transfer_time = 0.7*TIME_TOTOL/len(range(1913,1921,1))
        wait_time = 0.3*TIME_TOTOL/len(range(1913,1921,1))

        for new_year in range(1913,1921,1):
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

        #5:01;16
        self.wait()
        #5:02;16
        #update the contry circles from 1920 - 1950 :WW2
        TIME_TOTOL = 20 # 1.88 years per sec

        transfer_time = 0.7*TIME_TOTOL/len(range(1921,1951,1))
        wait_time = 0.3*TIME_TOTOL/len(range(1921,1951,1))

        for new_year in range(1921,1951,1):
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
        #5:22;16

        #pause at 1950
        self.wait(9)
        #5:29;16

        developping = VGroup()
        developped = VGroup()
        names_to_show = [
            "Yemen",#UP
            "Afghanistan",#UP
            "Saudi Arabia",#2*UP
            "China",#DOWN
            "India",#2*DOWN
            "United States",#1.5*UP
            "Switzerland"#1.5*DOWN
            ]
        next_to_mat = [1, 1, 2, -1, -2, 1.5, -1.5]
        dict_to_show = {}
        run_time_mat =[2, 1.5, 6, 3, 3, 2.5, 5]
        color_mat = [RED,RED,RED,RED,RED,BLUE,YELLOW]

        for area in areas:
            for i,contry in enumerate(area.contry_list):
                position = contry.get_both_fertandlife_point(1950)
                
                # if x is life_expectancy, y is fertality,
                # then I define that line: 0.124285714285714 * x - 2.48571428571429
                # this line passes two points [20,0] and [90,8.7]
                # then I define if a country is at left-up part of the line, 
                # its developpping country
                # else is developped
                if 0.124285714285714 * position[0] - 2.48571428571429 > position[1]:
                    developping.add(contry.shape)
                else:
                    developped.add(contry.shape)

                if contry.name in names_to_show:
                    dict_to_show[contry.name] = contry

        #show developping countries and developped countries
        #5:29;16
        self.play(
            ApplyWave(
                developping,
                amplitude = 0.5,
                run_time = 2,
                rate_func =there_and_back
                )
            )
        #5:31;16
        self.wait()
        #5:33;16
        self.play(
            ApplyWave(
                developped,
                amplitude = 0.5,
                run_time = 2,
                rate_func =there_and_back
                )
            )
        #5:35;16

        self.wait()
        #high light some cuntries:
        lables = []
        lables1 = []
        for i,name in enumerate(names_to_show):
            lables.append(TextMobject(online_translation(name),color = color_mat[i]).scale(0.1))
            lables[i].move_to(dict_to_show[name].shape.get_center())
            lables1.append(TextMobject(online_translation(name),color = color_mat[i]).scale(0.7))
            lables1[i].next_to(dict_to_show[name].shape,next_to_mat[i]*UP)

            fadein_time = 0.1*run_time_mat[i]
            transform_time = 0.5*run_time_mat[i]
            wait_times = 0.4*run_time_mat[i]

            self.play(FadeIn(lables[i]),run_time = fadein_time)
            self.play(
                AnimationGroup(
                    WiggleOutThenIn(
                        dict_to_show[name].shape,
                        scale_value = 1.5
                        ),
                    ReplacementTransform(lables[i],lables1[i]),
                    run_time = transform_time
                    )
                )
            self.wait(wait_times)

        lables = VGroup()
        for lable in lables1:
            lables.add(lable)
        self.play(FadeOut(lables))

        #update the contry circles from 1950 - 2018:

        TIME_TOTOL = 22

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
        #06:22:05

        self.wait(11)

        #06:33;05
        



        animations = []
        for mob in self.mobjects:
            if isinstance(mob,Mobject) & (not hasattr(mob,"asdfi")):
                animations.append(FadeOut(mob))

        self.play(*animations)
        self.wait() 
