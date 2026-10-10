function [new_places] = ant_tour_construction(start_places, colony_size, a_priori, tau, alpha, beta)
% SUMMARY: This function completes the ant tour matrix for one iteration.
%   For each ant in the colony, we make them traverse the whole map (tour). 
%   They first start at a randomly generated starting area (start_places), 
%   and jump to each node. The jumps are controlled by the attractiveness 
%   of the node raised to beta, and the pheromone effect raised to alpha. 

for i = 1:colony_size   % For each ant...
    a_priori_temp = a_priori;   % ... we track its sight// sight is what it saw, or what cities it saw. 
    for j = 1:51                % We then have it move around the 51 cities (not 52 because 1 is already starting point).
        c = start_places(i,j);      % We track its place and put it into c.
        a_priori_temp(:,c) = 0;
        temp = (tau(c,:).^alpha).*(a_priori_temp(c,:).^beta);
        s = (sum(temp));
        p =(1/s).* temp;
        r = rand; % rand just generates from 0 to 1. 
        s = 0;
        for k = 1:52
            s = s + p(k);
            if r <= s
                start_places(i,j+1)=k;
                break
            end
        end
    end
end
new_places = start_places;