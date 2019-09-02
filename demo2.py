from mainm.Danim.Contry import *

#create the axes with logscale x axis that match the "log scale axis settings" in Contry.py
def create_logsclae_axes(tick_numbers = None, factor = LOG_FACTOR,base = LOG_BASE, origin = dis_NEWORIGIN):
    axes = Axes(

        x_min = dis_xmin,
        x_max = dis_xmax,
        y_min = dis_ymin,
        y_max = dis_ymax,
        x_tick_frequency = 100,
        x_axis_config = {
            "leftmost_tick" : -1,
            "is_log_scale" : True,
            "number_scale_val": 0.7,
            "log_factor": factor,
            "log_base":base
            }
        )
    axes.y_axis.move_to(ORIGIN,aligned_edge=DOWN)
    axes.x_axis.stretch_about_point(dis_x_axis_stretch_factor, 0, ORIGIN)
    #axes.x_axis.shift(x_axis_shift_factor)
    #axes.y_axis.stretch_about_point(dis_y_scale_factor, 1, ORIGIN)
    axes.shift(origin)

    #------------------------------------------------------------------------------------

    # set up the appropriate log scale numberline to represent the x axis:-------------
    if not tick_numbers == None:
        for number in tick_numbers:
            axes.x_axis.add_tick(number,axes.x_axis.tick_size, is_log_num = False)
            if number < 1:
                axes.x_axis.decimal_number_config['num_decimal_places'] = 1
                axes.x_axis.add_numbers(number,is_log_num = False)
            
            else:
                axes.x_axis.decimal_number_config['num_decimal_places'] = 0
                axes.x_axis.add_numbers(number,is_log_num = False)

    #adjust the axes:
    axes.y_axis.shift(LEFT*5.5+DOWN)
    return axes


class TryShape(Scene):
    def construct(self):


        # Create the axes--------------------------------------------------------------------
        axes = create_logsclae_axes(tick_numbers = [0.2,0.5,1,2,5,10,20,50,100,200])
        #adjust the axes:
        axes.y_axis.shift(LEFT*5.5+DOWN)
        x_axis_lable1 = TextMobject("人均收入",tex_to_color_map={"人均收入": BLUE})
        x_axis_lable2 = TextMobject("(国际元/天)",tex_to_color_map={"(国际元/天)": BLUE})
        x_axis_lable1.scale(0.7)
        x_axis_lable1.move_to(2.9*DOWN+6.3*RIGHT)
        x_axis_lable2.scale(0.7)
        x_axis_lable2.next_to(x_axis_lable1,DOWN)

        #add year_lable
        year_lable = Integer(2016,group_with_commas = False,color = TEAL_E).scale(1.5)
        year_lable.to_edge(UR)
        self.play(ShowCreation(VGroup(axes,x_axis_lable1,x_axis_lable2,year_lable)),run_time = 3)
        self.wait()

        axis = NumberLine(x_min = -4,x_max = 4)

        '''
        india = Contry("India", "Distribution")
        india.set_the_contry_distribution(1900)
        new_shape = india.shape.deepcopy()
        india.shape.fit_to_new_axes(axes)
        self.play(ShowCreation(VGroup(india.shape,axis,new_shape)))

        '''
        american = Contry("United States","Distribution")
        american.set_the_contry_distribution(2016,color = BLUE)
        american.shape.fit_to_new_axes(axes)
        self.play(ShowCreation(VGroup(american.shape)))

        china = Contry("China", "Distribution")
        china.set_the_contry_distribution(2016,color = RED)
        china.shape.fit_to_new_axes(axes)
        

        dots = VGroup()
        for shape in [china.shape,american.shape]:
            dots.add(Dot(np.array([shape.x_max,0,0]),color = GREEN))
            dots.add(Dot(np.array([shape.x_min,0,0]),color = GREEN))
            dots.add(Dot(np.array([shape.mean,0,0]),color = GREEN))
        '''
        if isinstance(china.shape,NormalDistribution):
            is_overlap, overlap_range = is_over_lap(
                american.shape.x_min,
                american.shape.x_max,
                china.shape.x_min,
                china.shape.x_max
                )


            new_anchors = american.shape.get_anchors()
            dis2_anchors = china.shape.get_anchors()
            
            # add edge point as new anchor point 
            new_anchors_x = copy.deepcopy(overlap_range)
            #deepcopy so that any change in new_anchors_x would not affect overlap_range

            #change attributes .highest_points
            american.shape.highest_points = np.array([american.shape.highest_points,china.shape.highest_points])        

            for point in dis2_anchors:
                if is_in_range(point[0],overlap_range[0],overlap_range[1]) and not point[0] in new_anchors_x:
                    new_anchors_x.append(point[0])
            
            
            for i,x in enumerate(new_anchors_x):
                print(i,x,x in new_anchors[:,0])
            
            print("start")
            print(new_anchors_x[0])
            print(new_anchors[0][0])
            #new_anchors = american.shape.insert_new_anchor_by_x(new_anchors_x,new_anchors,multiple_xs = True)

            # raise the new anchor:
            for i,anchor in enumerate(new_anchors):
                # if anchor point is within the overlap range
                if is_in_range(anchor[0],overlap_range[0],overlap_range[1],include_edge = True):

                    anchor[1] += china.shape.get_distribution_value_by_x(anchor[0])

        '''
        american.shape.stack_over(china.shape)
        self.play(ShowCreation(VGroup(china.shape,american.shape,dots,axis)))


class MainScene(Scene):
    def construct(self):
        self.IntroduceTheContryDistribution()
        self.CompareBetweenContries()


    def IntroduceTheContryDistribution(self):
        # To show how the original income distribution looks like: 

        introduce1 = TextMobject("如果横轴表示日均收入水平")
        introduce1.shift(2*UP)
        introduce2 = TextMobject("那么中国的人均收入分布就是这样...")
        introduce2.next_to(introduce1,DOWN)

        #create non-logscale axes
        axes = Axes(

            x_min = 0,
            x_max = 16,
            y_min = 0,
            y_max = 1,
            )

        
        axes.y_axis.stretch_about_point(15,1,ORIGIN)
        #axes.x_axis.stretch_about_point(0.5,0,ORIGIN)
        axes.x_axis.add_numbers(*range(0,17,1))
        for number in axes.x_axis.numbers:
            number.set_value(number.get_value()*150)
        axes.x_axis.numbers.shift(0.03*LEFT)
        axes.shift(3*DOWN+6.6*LEFT)

        
        lable1 = TextMobject("人均每日收入",tex_to_color_map={"人均每日收入":BLUE})
        lable2 = TextMobject("(人民币元/天)",tex_to_color_map={"(人民币元/天)":BLUE})
        lable1.scale(0.7)
        lable2.scale(0.7)
        lable1.shift([5.5,-1.5,0])

        start_point = lable2.get_critical_point(UP+LEFT)
        end_point = lable1.get_critical_point(LEFT+DOWN)
        lable2.shift(end_point - start_point + np.array([0,-0.2,0]))
        lable = VGroup(lable1,lable2)

        self.play(
            AnimationGroup(
                ShowCreation(axes.x_axis),
                Write(lable),
                Write(introduce1)
                ),
            run_time = 2
            )
        self.wait()
        self.play(Write(introduce2))

        # Lognormal distribution with mean 139 RMB/day:
        loggraph = axes.get_graph(lognormal_pdf,x_min = 0.01,fill_color = RED,color = RED,opacity = 0.3)
        self.play(ShowCreation(loggraph),run_time = 2)
        self.wait()

        self.play(FadeOut(VGroup(introduce1,introduce2)))

        #create the logscale x axis:
        logscale_axis = create_logsclae_axes(tick_numbers = [1,3,20,30,50,100,150,300,800,3000],factor = 3).x_axis

        # before transform the x axis into logsclae,
        # store the logscale distribution graph in the variable logged_graph

        logged_graph = FunctionGraph(normal_pdf_custom,color = RED,opacity = 0.3)
        logged_graph.points[:,1] *= 10
        shift_vec1 = [dis_NEWORIGIN[0],axes.x_axis.number_to_point(0)[1],0]
        logged_graph.shift(shift_vec1)


        # Transform the x axis to logscale
        shift_vec2 =[-3.5,axes.x_axis.number_to_point(0)[1] - logscale_axis.number_to_point(5)[1],0]
        logscale_axis.shift(shift_vec2)
        logscale_axis.main_line.shift([3.5,0,0])
        logscale_axis.tip.shift([3.5,0,0])


        #introducing the logscale axis:
        introduce1 = TextMobject("如果将横轴变为对数形式")
        introduce1.shift(3*UP)
        self.play(Write(introduce1))
        self.wait()
        self.play(ReplacementTransform(axes.x_axis,logscale_axis),run_time = 1.5)

        # Transform the graph to logscale:
        introduce2 = TextMobject("那么中国的人均收入分布就变为正态分布")
        introduce2.next_to(introduce1,DOWN)
        self.play(
            AnimationGroup(
                ReplacementTransform(loggraph,logged_graph),
                Write(introduce2),
                run_time = 2
                )
            )

        self.wait()
        self.play(FadeOut(VGroup(introduce1,introduce2)))

        #calculate the 99.5%percentile points
        #1.29 is the mean 
        z999 = inverse_of_normal_cdf(0.995)
        x1 = - z999 + 1.29
        x2 = z999 +1.29
        y = normal_pdf_custom(x1)*10 + shift_vec1[1]
        
        x1 += dis_NEWORIGIN[0]
        x2 += dis_NEWORIGIN[0]

        #create the line that mark the 99.5% percent area
        hline = Line([-5,y,0],[7,y,0],color = RED)
        introduce1 = TextMobject("为了直观 我们取图像中间百分之99.5的区域")
        introduce1.shift(3*UP)


        self.play(Write(introduce1),run_time = 1.5)
        self.play(ShowCreation(hline))
        self.wait(0.6)


        # lable the 2 edge points
        left_most = np.array([x1,y,0])
        right_most = np.array([[x2,y,0]])
        
        #create the new graph
        new_graph = NormalDistribution(color = RED, fill_opacity = 0.3,set_up_the_bot_curve= True)
        anchors = logged_graph.get_anchors()
        for i in range(len(anchors)-1):
            if is_in_range(x1,anchors[i][0],anchors[i+1][0],include_edge = True):
                start_index = i+1
            if is_in_range(x2,anchors[i][0],anchors[i+1][0],include_edge = True):
                end_index = i + 1
        new_anchors = np.append(anchors[start_index:end_index],right_most,axis = 0)
        new_anchors = np.insert(new_anchors,0,left_most,axis = 0)

        h1, h2 = get_smooth_handle_points(new_anchors)
        arrays = [h1, h2, new_anchors[1:]]

        up_curve_points = np.zeros(((len(new_anchors)*3 - 2),3))
        up_curve_points[0] = new_anchors[0]

        for index, array in enumerate(arrays):
            up_curve_points[index + 1::3] = array

        bot_curve_points = np.zeros((3,3))
        bot_curve_points[:,1] = y
        bot_curve_points[:,0] = np.linspace(x2, x1, 4)[1:]

        new_points = np.append(up_curve_points,bot_curve_points,axis = 0)
        new_graph.points = new_points

        self.play(
            AnimationGroup(
                FadeOut(VGroup(logged_graph,hline)),
                FadeIn(new_graph)),run_time = 3
            )
        self.wait(2)
        self.play(new_graph.shift,np.array([0,shift_vec1[1]-y,0]))
        self.wait()

        # adjust the heights to represents the total population:
        self.play(FadeOut(introduce1))

        introduce1 = TextMobject("伸缩收入分布图表示国家人口总数量")
        introduce1.shift(3.6*UP)
        introduce1.to_edge(LEFT)
        introduce2 = TextMobject("中国人口数量为:")
        introduce2.next_to(introduce1,DOWN)
        introduce2.to_edge(LEFT)

        pop_lable = DecimalNumber(13.9,
            show_ellipsis=False,
            num_decimal_places=1,
            include_sign=False)
        pop_lable.next_to(introduce2,RIGHT)

        introduce3 = TextMobject("亿")
        introduce3.next_to(pop_lable)

        introduce = VGroup(introduce1,introduce2,introduce3,pop_lable)
        self.play(Write(introduce))
        self.wait()
        # index choice does not matter
        i = 7
        y_min = logscale_axis.number_to_point(5)[1]
        factor = 13.9/(new_graph.get_anchors()[i][1] - y_min)
        pop_lable.add_updater(
            lambda d: d.set_value(
                (new_graph.get_anchors()[i][1] - y_min)*factor
                )
            )
        self.add(pop_lable)
        bot_point = new_graph.get_critical_point(DOWN)
        self.play(new_graph.stretch_about_point,0.5,1,bot_point,run_time = 3)
        
        self.wait(0.8)
        self.play(new_graph.stretch_about_point,2.5,1,bot_point,run_time = 3)
        
        self.wait(2)
        self.play(FadeOut(VGroup(new_graph,introduce,logscale_axis,lable)))


    def CompareBetweenContries(self):
        introduce1 = TextMobject("为了比较不同国家之间的收入分布")
        introduce1.shift(3*UP)
        introduce2 = TextMobject("我们用国际元替代人民币表示收入")
        introduce2.next_to(introduce1,DOWN)

        self.play(Write(introduce1),run_time = 1.5)
        self.play(Write(introduce2),run_time = 1.5)
        self.wait()
        self.play(FadeOut(VGroup(introduce1,introduce2)))

        # Create the axes--------------------------------------------------------------------
        axes = create_logsclae_axes(tick_numbers = [0.2,0.5,1,2,5,10,20,50,100,200])
        #adjust the axes:
        axes.y_axis.shift(LEFT*5.5+DOWN)
        x_axis_lable1 = TextMobject("人均收入",tex_to_color_map={"人均收入": BLUE})
        x_axis_lable2 = TextMobject("(国际元/天)",tex_to_color_map={"(国际元/天)": BLUE})
        x_axis_lable1.scale(0.7)
        x_axis_lable1.move_to(2.9*DOWN+6.3*RIGHT)
        x_axis_lable2.scale(0.7)
        x_axis_lable2.next_to(x_axis_lable1,DOWN)

        #add year_lable
        year_lable = Integer(2016,group_with_commas = False,color = TEAL_E).scale(1.5)
        year_lable.to_edge(UR)
        self.play(ShowCreation(VGroup(axes,x_axis_lable1,x_axis_lable2,year_lable)),run_time = 3)
        self.wait()
        #------------------------------------------------------------------------------------

        #Distribution Graph:------------------------------------------------------------------------


        #create the contry income distributions
        china = Contry("China", "Distribution")
        china.set_the_contry_distribution(2016)

        # kind of too long, but only for demo
        
        end_point = axes.x_axis.number_to_point(china.shape.mean)
        start_point = np.array([china.shape.mean,0,0])
        shift_vec = end_point - start_point
        
        china.shape.fit_to_new_axes(axes)
        china.shape.shift(-shift_vec)


        #Show the China distribution with name lable
        china_lable = TextMobject("中国")
        china_lable.next_to(china.shape,UP)
        self.play(FadeIn(VGroup(china_lable,china.shape)),run_time = 2)
        self.wait()

        self.play(AnimationGroup(FadeOut(china_lable),ApplyMethod(china.shape.shift,shift_vec)),run_time = 2)
        self.wait()
        
        # add autimate update words and vertical line:
        introduce1 = TextMobject("中国人均日收入为:") 
        introduce1.shift(UP+0.5*LEFT)
        introduce2 = DecimalNumber(
                    axes.x_axis.point_to_number(china.shape.get_mean_point(),return_log_num = False),
                    show_ellipsis=False,
                    num_decimal_places=1,
                    include_sign=False
                )
        introduce2.next_to(introduce1,RIGHT)
        
        introduce3 = TextMobject("国际元")
        introduce3.next_to(introduce2,RIGHT)

        #create the second line of introduction
        introduce4 = TextMobject("相当于")
        start_point = introduce4.get_critical_point(UP+LEFT)
        end_point = introduce1.get_critical_point(LEFT+DOWN)
        introduce4.shift(end_point - start_point + np.array([0,-0.2,0]))

        introduce5 = DecimalNumber(
                    introduce2.get_value()*EXCHANGE_RATE_FOR_RMB_TO_INTERNATIONAL_DOLLAR,
                    show_ellipsis = False,
                    num_decimal_places=1,
                    include_sign=False
                )
        introduce5.next_to(introduce4,RIGHT)

        introduce6 = TextMobject("元人民币")
        introduce6.next_to(introduce5,RIGHT)

        introduce = VGroup(introduce1,introduce2,introduce3,introduce4,introduce5,introduce6)

        self.play(Write(introduce),run_time = 2)
        self.wait()
        
        #update the distribution:
        
        for year in [2010,2005,2000]:
            self.play(
                AnimationGroup(
                    china.get_update_single_contry_distribution_animation(year, axes = axes),
                    ApplyMethod(year_lable.set_value,year),
                    ApplyMethod(introduce2.set_value,axes.x_axis.point_to_number(china.shape.get_mean_point(),return_log_num = False)),
                    ApplyMethod(introduce5.set_value,axes.x_axis.point_to_number(china.shape.get_mean_point(),return_log_num = False)*EXCHANGE_RATE_FOR_RMB_TO_INTERNATIONAL_DOLLAR)
                    ),
                run_time = 2
                )
            self.wait()

        # make comparison among different contrys

        self.play(FadeOut(introduce))

        self.wait()

        self.play(
            AnimationGroup(
                china.get_update_single_contry_distribution_animation(2016, axes = axes),
                ApplyMethod(year_lable.set_value,2016),
                run_time = 2
                )
            )


        self.wait()

        #create the distributions for other two contries
        american = Contry("United States","Distribution")
        american.set_the_contry_distribution(2016,color = BLUE)

        american.shape.fit_to_new_axes(axes)

        american.shape.shift(3*UP)        

        #Show the American distribution with name lable 
        #and stack the shape upon the distribution of china
        american_lable = TextMobject("美国")
        american_lable.next_to(american.shape,UP)

        #and stack the shape upon the distribution of china
        self.play(FadeIn(VGroup(american_lable,american.shape)))
        self.wait()
        self.play(AnimationGroup(american.get_stack_over_animation(china.shape),FadeOut(american_lable)))
        
        stacked = NDGroup(china.shape,american.shape)

        #Show the India distribution with name lable 
        #and stack the shape upon the distribution of china
        india = Contry("India","Distribution")
        india.set_the_contry_distribution(2016,color = YELLOW)

        india.shape.fit_to_new_axes(axes)
        india.shape.shift(-shift_vec)   


        #Show the india distribution with name lable
        india_lable = TextMobject("印度")
        india_lable.next_to(india.shape,UP)

        #and stack the shape upon the distribution of china
        self.play(FadeIn(VGroup(india_lable,india.shape)))

        self.play(AnimationGroup(india.get_stack_over_animation(stacked),FadeOut(india_lable)))


        self.wait()
                #compare the income distribution back in 1800
        contries = Area(init_by_areaname = False, contry_list = [china,american,india])
        self.play(
            AnimationGroup(
                contries.update_stacked_distributions_by_year_animation(1900,axes = axes),
                ApplyMethod(year_lable.set_value,1900),
                run_time = 2
                )
            )
        
        #create and show the extreme poverty line:
        #definition: an income below the international 
        #poverty line of $1.90 per day (in 2011 prices)
        start = np.array([axes.x_axis.number_to_point(1.9,is_log_num= False)[0],-3.8,0])
        end = np.array([start[0],2,0])
        vline = DashedLine(start,end,color = GREEN,dashed_segment_length = 0.1)
        
        introduce1 = TextMobject("这是极端贫困线", color = GREEN, fill_opacity = 1).scale(0.6)
        introduce1.next_to(vline,UP)
        introduce1.shift(0.5*UP)
        introduce2 = TextMobject("收入低于1.9国际元/日", color = GREEN, fill_opacity = 1).scale(0.6)
        introduce2.next_to(introduce1,DOWN)
        introduce2.shift(0.2*UP)
        introduce = VGroup(introduce1,introduce2)

        self.play(
            AnimationGroup(
                ShowCreation(vline),
                Write(introduce)
                )
            )
        

        #compare the income distribution back in 1800 1900 2000 2010 2015 2017 2018:
        for year in [1800,1900,2000,2010,2015,2017,2018]:
            self.play(
                AnimationGroup(
                    contries.update_stacked_distributions_by_year_animation(year,axes = axes),
                    ApplyMethod(year_lable.set_value,year),
                    run_time = 2
                    )
                )
            self.wait()

        shapes = VGroup()
        for contry in contries.contry_list:
            shapes.add(contry.shape)

        self.play(FadeOut(VGroup(shapes,introduce)))
        self.wait(2)




