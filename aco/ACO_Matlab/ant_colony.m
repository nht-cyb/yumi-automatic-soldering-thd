clearvars;


%% =================== Part 0: Parameter setting =====================================
iterations = 500;           % Sets the number of iterations where the algorithm will run.
colony_size = 60;           % Sets the number of ants in the colony.
evap_coeff = 0.1;          % Sets the evaporation coefficient that will be used in updating the pheromone (must be between 0 and 1).

alpha = 1;                  % Sets the bias of using pheromone deposits in the decision process. 
                            % (Heuristic parameter describing how greedy the algorithm is in finding its path across the graph.)
                            % Exploitationn parameter - set this to 0 and
                            % the algo becomes greedy (random spikes). Set this high and it
                            % will just dig deep to the local optima. The
                            % problem is that it may find not good answers
                            
beta = 4;  %12                % Sets the bias for deciding if a shorter path is better.
                            % (Heuristic parameter describing how fast the ants are going to converge to a steady solution.) 
                            % Exploration parameter - set this to 0 and
                            % the attractiveness of the moves becomes
                            % neglected. It will just keep digging deep
                            % into the local optima. 

tau = 0.0001 * ones(52);    % We create a 52 x 52 tau matrix full of 1. We initialize it to a very small value (not 0 because it will 
                            % cause the system to divide by 0 later, which is
                            % bad. 
                         
el=0.97;                     % Set the parameter for eliminating common costs. 

Q = 0.2;                     % Positive constant used for updating tau. To control the level of exploration
                             % undertaken by the ants
                             % History: 1/10000 (11/25/2016) Answer: 8000 range

%% =================== Part 0.1: Load berlin52 dataset from csv file ===================
cd('Q:\Thesis\Code\ACO_Matlab')
berlin52 = csvread('berlin52.csv');
x = berlin52(:,1);
y = berlin52(:,2);


%% =================== Part 0.2: Plot berlin52 dataset ==================================
figure
hold on;

subplot(2,2,1);
mycolor = [0.93,0.273,0.191];
plot(x,y,'o','MarkerFaceColor','k','MarkerEdgeColor','b','MarkerSize',5)
title('Do thi bieu dien dataset')
xlabel('x  (mm)')
ylabel('y  (mm)')
axis square

%% =================== Part 1: Initialize parameters ====================================

% Generate distance for each node

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

for i=1:iterations % We run the ant system algorithm with {iterations} number of iterations.
    % ---------- Part 2.1 Randomly Generate Places for each ant -----------
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
    title('Do dai quang duong trung binh theo so vong lap');
    xlabel('So vong lap');
    ylabel('Quang duong  (mm)');
    axis square
    
    % Plot Ant Behaviour
    subplot(2,2,4);
    plot(iteration,mean_cost);
    title('Quang duong tai moi vong lap');
    xlabel('Vong lap');
    ylabel('Quang duong  (mm)');
    axis square
    
    
   % Plot the best route
    [k,l]=min(min_cost);
    for i=1:52+1
    X(i)=x(besttour(l,i));
    Y(i)=y(besttour(l,i));
    end
    subplot(2,2,2);
    plot(X,Y,'--ko','MarkerEdgeColor','k','MarkerFaceColor','g','MarkerSize',5)
    grid on;
    xlabel('x  (mm)');ylabel('y  (mm)');
    title(['Quy dao ngan nhat = ',num2str(k)]);
    %dim = [.9 .2 .6 .6];
    %str = {'Parameters',strcat('\alpha: ', num2str(alpha)), strcat('\beta: ', num2str(beta)), strcat('m: ', num2str(colony_size)), strcat('Q: ', num2str(Q)), strcat('\rho: ',num2str(evap_coeff))};
    %annotation('textbox',dim,'String',str,'FitBoxToText','on')
    axis square 
    
    pause(.1) %// pause 0.1 seconds to slow things down
    drawnow  
end