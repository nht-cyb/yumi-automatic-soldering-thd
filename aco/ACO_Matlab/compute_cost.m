function [cost, reference] = compute_cost(colony_size, distance_matrix, tour, el)
% SUMMARY: This function computes the cost of traversed by the ant, and the
% amount of tau that must be decayed.
%   For each ant, we look at the path it took <<tour>>, and then we base
%   the distance from the distance matrix and add it to the link.

for i = 1:colony_size % For each ant,...
    dist = 0;
    for j=1:52
        dist = dist + distance_matrix(tour(i,j),tour(i,j+1)); % ...we look at the tour table, then get the distance traversed with the help of distance_matrix, and store it in s.
    end
    reference(i)= dist; % ... we make a reference table, for ant 1, we have a cost of 1 (dist) and so on.
end
cost = reference; 
reference = reference - el * min(reference); % ... eliminates repeating distances