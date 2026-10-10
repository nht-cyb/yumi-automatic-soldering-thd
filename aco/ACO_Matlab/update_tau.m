function [tau]=update_tau(colony_size, tau, tour, reference, evap_coeff, Q)
%SUMMARY: The idea here is that we update the pheromones. We take into
%consideration the evaporatoin coefficient.
%   Here, we're using Ant-Quantity AS variation. In this case, only local information, d_{ij} , is used to update pheromone 
%   concentrations. Lower cost links are made more desirable. If d_{ij} represents the distance between links, then ant-quantity AS 
%   prefers selection of the shortest links.

for i= 1:colony_size % For each ant...
    for j=1:52 % ... we update certain values of tau depending on the tour table
        delta_tau = Q/reference(i); % This is an Ant-Quantity AS
        tau(tour(i,j),tour(i,j+1)) = (1-evap_coeff) * tau(tour(i,j),tour(i,j+1)) + delta_tau;
    end
end