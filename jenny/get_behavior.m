function roca_vec = get_behavior(trial)


dur_to_plot = [800];
mod_depth = [0 6 16 28 40 60 80 100];

hit_indx = find(strcmp(trial.result,'H'));
miss_indx = find(strcmp(trial.result,'M'));
fa_indx = find(strcmp(trial.result,'FA'));
cr_indx = find(strcmp(trial.result,'CR'));

for i = 1:length(dur_to_plot)
    curr_dur = dur_to_plot(i);
    dur_indx = find(trial.stimdur == curr_dur);
    
    % get fa rate
    curr_depth = 0;
    depth_indx = find(trial.moddepth == curr_depth);
    non_target_indx = intersect(depth_indx,dur_indx);
    curr_fa_indx = intersect(non_target_indx,fa_indx);
    fa_rate = length(curr_fa_indx)/length(non_target_indx);
    roca_vec(1,i) = 0.5;
    for j = 2:length(mod_depth)
        curr_depth = mod_depth(j); 
        depth_indx = find(trial.moddepth == curr_depth);
        curr_stim_indx = intersect(dur_indx,depth_indx);
        curr_hit_indx = intersect(curr_stim_indx,hit_indx);
        curr_miss_indx = intersect(curr_stim_indx,miss_indx);
        hit_rate = length(curr_hit_indx)/length(curr_stim_indx);
        roca_vec(j,i) = (1+hit_rate-fa_rate)/2;
    end
end







