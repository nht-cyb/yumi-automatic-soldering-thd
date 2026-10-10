%**************************************************************************
%           CI: Travelling Salesman Problem using ACO [AS Variation]
% -------------------------------------------------------------------------
                       
clearvars;


%% =================== Part 0: Cai dat tham so =====================================
iterations = 500;           % So vong lap
colony_size = 60;           % So kien
evap_coeff = 0.1;           % He so bay hoi

alpha = 15;                 % He so tham lam cho thuat toan, muc thay doi tu 0 ->
                            
beta = 20;  %12             % he so xet muc do bao hoa cua viec tim kiem
                          

tau = 0.0001 * ones(52);    % tao ma tran khoang cach ban dau co 52x52, gtri xap xi 0
                           
                         
el=0.97;                     % tham so loai bo chi phi thong thuong

Q = 0.2;                     % hang so duong cap nhat tau, chi muc do kham pha cua kien
                        

%% =================== Part 0.1: Load berlin52 dataset from csv file ===================
cd('D:\Work\N4\TUH\Report2\TH2')
berlin52 = csvread('berlin52.csv');
x = berlin52(:,1);
y = berlin52(:,2);


%% =================== Part 0.2: Plot berlin52 dataset ==================================
figure
hold on;

subplot(2,2,1);
mycolor = [0.93,0.273,0.191];
plot(x,y,'o','MarkerFaceColor',mycolor,'MarkerEdgeColor','k','MarkerSize',5)
title('Plot of Berlin52 Dataset')
xlabel('x  (km)')
ylabel('y  (km)')
axis square

%% =================== Part 1: Initialize parameters ====================================

% Khoi tao khoang cach

for i=1:52
    for j=1:52
        distance_matrix(i,j)=sqrt((x(i)-x(j))^2+(y(i)-y(j))^2);
    end
end

% Generate a priori attractiveness

for i=1:52
    for j=1:52
        if distance_matrix(i,j)==0
            a_priori(i,j)=0;
        else
            a_priori(i,j)=1/distance_matrix(i,j);
        end
    end
end

%% =================== Part 2: Ant System Algorithm ====================================

for i=1:iterations  % Chay cho n vong lap
    % ---------- Part 2.1 khoi tao dia diem di den ngau nhien cho dan kien -----------
    for j = 1:colony_size
        start_places(j,1) = fix(1+rand*(52-1));     % fix() rounds each element toward 0.
    end
    % ---------- Part 2.2 Probabilistic solution construction -------------
    [tour] = ant_tour_construction(start_places, colony_size, a_priori, tau, alpha, beta);
    tour = horzcat(tour,tour(:,1));                 % horzcat() concatenates arrays horizontally.
    
    % ---------- Part 2.3 Calculate the total distance traversed-----------
    [cost,reference] = compute_cost(colony_size, distance_matrix, tour, el);
    [tau] = update_tau(colony_size, tau, tour, reference, evap_coeff, Q);
    average_cost(i) = mean(cost);
    
    % ---------- Part 2.4 Find optimized route ----------------------------
    [min_cost(i), best_index] = min(cost);
    besttour(i,:) = tour(best_index,:);
    iteration(i) = i;
    mean_cost(i) = mean(cost);
    a(i)=min(min_cost);
    
    %% =================== Part 3: Plot results ============================================
    
    % Plot Average of tour distance vs Number of Iterations
    subplot(2,2,3);
    %plot(iteration,min_cost);
    %plot(iteration,mean_cost);
    plot(iteration,a);
    title('Tour vs Iterations');
    xlabel('Iterations');
    ylabel('Tour');
    axis square
    
    % Plot Ant Behaviour
    subplot(2,2,4);
    plot(iteration,mean_cost);
    title('Ant Behaviour');
    xlabel('Iterations');
    ylabel('Tour');
    axis square
    
    
   % Plot the best route
    [k,l]=min(min_cost);
    for i=1:52+1
    X(i)=x(besttour(l,i));
    Y(i)=y(besttour(l,i));
    end
    subplot(2,2,2);
    plot(X,Y,'--ko','MarkerEdgeColor','k','MarkerFaceColor',[1 1 0],'MarkerSize',5)
    grid on;
    xlabel('x (km)');ylabel('y (km)');
    title(['Cost = ',num2str(k)]);
    %dim = [.9 .2 .6 .6];
    %str = {'Parameters',strcat('\alpha: ', num2str(alpha)), strcat('\beta: ', num2str(beta)), strcat('m: ', num2str(colony_size)), strcat('Q: ', num2str(Q)), strcat('\rho: ',num2str(evap_coeff))};
    %annotation('textbox',dim,'String',str,'FitBoxToText','on')
    axis square 
    
    pause(.1) %// pause 0.1 seconds to slow things down
    drawnow  
end

