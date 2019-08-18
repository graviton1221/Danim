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



class MainScene(Scene):
    def construct(self):
        
        title1 = TextMobject("如何直观地显示五维数据?")
        title2 = TextMobject("如果用一个圆代表一个国家, 圆的面积大小表示人口...")

        self.play(Write(title1))
        self.wait()
        self.play(FadeOut(title1))
        self.play(Write(title2))
        self.wait()
        self.play(FadeOut(title2))

        china = Contry("China",show_CN_name = True)
        chinaG = china.fill_data_set_the_circle_then_group(color= RED,show_CN_pop_lable = True)
        self.play(GrowFromCenter(chinaG))
        self.wait(1.5)
        
        bangladesh = Contry("Bangladesh",show_CN_name = True)
        bangladeshG = bangladesh.fill_data_set_the_circle_then_group(color= BLUE,show_CN_pop_lable = True)
        self.play(Transform(chinaG,bangladeshG),
            run_time = 1,replace_mobject_with_target_in_scene= True)
        self.wait(1.5)


        american = Contry("United States",show_CN_name = True)
        americanG = american.fill_data_set_the_circle_then_group(color = GREEN,show_CN_pop_lable = True)
        self.play(Transform(bangladeshG,americanG),
            run_time = 1, replace_mobject_with_target_in_scene= True)
        self.wait(1.5)
        
        
        india = Contry("India",show_CN_name = True)
        indiaG = india.fill_data_set_the_circle_then_group(color = PURPLE_A,show_CN_pop_lable = True)
        self.play(Transform(americanG,indiaG),
            run_time = 1,replace_mobject_with_target_in_scene= True)
        self.wait(1.5)
        

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

        
        #------------------创立标示年份的标签 并让圆心移动至相应年份的数据点处
        year_lable = Integer(2018,group_with_commas = False,color = TEAL_E).scale(1.5)
        year_lable.to_edge(UR)
        self.play(GrowFromCenter(year_lable),run_time =0.6)
        
        
        target_point = india.get_transfromed_fertandlife_point(year_lable.get_value())#target_point_in_2018

        self.play(
            VGroup(india.contry_name,india.population_lable,india.shape,india.population_lable_unit).shift,
            target_point - india.shape.get_center(),run_time = 1)  
        self.wait()

        dot = Dot(color = RED,radius = 0.03)
        dot.move_to(india.shape.get_center())
        self.play(FadeIn(dot),run_time = 0.5)

        #------------------创立实线 让其跟随圆心位置移动
        vline = Line(
            [target_point[0],NEWORIGIN[1],0],
            target_point,
            stroke_width = 2,
            stroke_color = RED
        )
        hline = Line(
            [NEWORIGIN[0],target_point[1],0],
            target_point,
            stroke_width = 2,
            stroke_color = RED
        )
        self.play(ShowCreation(VGroup(vline,hline)),run_time = 1)

        vline.add_updater(lambda v: v.set_points_as_corners([[dot.get_center()[0],NEWORIGIN[1],0], dot.get_center()]))
        hline.add_updater(lambda h: h.set_points_as_corners([[NEWORIGIN[0],dot.get_center()[1],0], dot.get_center()]))
        self.add(vline,hline,dot)

        #------------------创建二维坐标标签

        india.create_data_coordinate_lable(2018)
        self.play(
            ShowCreation(india.data_coordinate_lable),
            ShowCreation(india.data_x_lable),
            ShowCreation(india.data_y_lable),
            run_time = 1          
            )


        #------------------根据年份更新

        #self.play(india.get_the_namelable_circle_alignment_animation())

        for new_year in [1800,1900,2000,2010]:
            shift_vect = india.get_transfromed_fertandlife_point(new_year) - india.shape.get_center()

            self.play(
                india.update_the_circle_with_everything_turnon_animation(new_year, show_track = False, show_population_lable_in_graph =True),
                dot.shift,shift_vect,
                year_lable.set_value,new_year,
                run_time = 1.2
                )
            self.wait(1)

        self.play(FadeOut(VGroup(india.shape,india.contry_name,india.population_lable,india.population_lable_unit,vline,hline,dot,india.data_coordinate_lable,india.data_x_lable,india.data_y_lable)))

        self.wait(1)
        
        #----------------按照地区创建所有国家

        area_rect = []
        area_rect_lable = []
        areas = []
        for i,area in enumerate(THE_WHOLE_WORLD):

            areas.append(Area(area))
            area_rect.append(Rectangle(height = 0.2, width = 0.5,color = AREA_COLOR_MAP[i],fill_opacity = 1))
            
            if i == 0:
                area_rect[i].next_to(year_lable,2*DOWN)

            else:
                area_rect[i].next_to(area_rect[i-1],DOWN)
            area_rect_lable.append(TextMobject(CH_THE_WHOLE_WORLD[i]).scale(0.4))
            area_rect_lable[i].next_to(area_rect[i],LEFT)

            areas[i].generate_all_contry_circles(COLORMAT = [AREA_COLOR_MAP[i]],if_switch_on =False)
            self.play(*areas[i].get_creation_animation(),
                GrowFromCenter(area_rect[i]),
                Write(area_rect_lable[i])
                )   
        #-------------------------按照日期更新所有圆


        for new_year in range(1800,2018,1):
            area_animation = []
            contry_name_anim = []
            for area in areas:
                area_animation += area.update_area_contryname_by_year_animation(new_year)
                area_animation += area.update_area_circles_by_year_animation(new_year)
                # SEQUENCE matters
                    
            self.play(
                *area_animation,
                year_lable.set_value,new_year,
                run_time = 0.5
                )
            self.wait(1.2)

        
            
