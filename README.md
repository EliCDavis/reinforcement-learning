# Reinforcement Learning

This repository aims to personally explore different reinforcement learning (RL) techniques implemented by hand to solve problems inside [Open AI's Gym](https://gym.openai.com). Lesson's learned from experimenting with different techniques will be documented. This repository should not be seen as a starting point for those wishing to learn about RL.

# Acrobat V1

## Monte Carlo: Default Reward, 3 numbers of precision

Monte Carlo method was implemented to update the value of actions the agent is allowed to take at the end of an episode. This method was able to get a succesful episode within around 100 episodes of training. 

![Monte Carlo](http://i.imgur.com/WKxfy8l.png)

It seems that the frequency in which succesful  episodes occur increases slightly over time. However the amount of time it takes to complete a single episode is seemingly random. Since the simulation is limited to 500 time steps, it's impossible to tell as to whether or not the max-time needed to solve an episode is decreasing over time.

In 10,000 iterations there was 147 solved episodes.

## Monte Carlo: -1/1 Reward, 3 numbers of precision

I thought maybe that the default reward does not adequetly reward the agent, as it's -1 for bad states, and 0 for successful states. I changed this to instead give a value of 1 as a reward for a successful state in hopes to coax the agent faster towards better solutions.

![Monte Carlo](https://i.imgur.com/8ln211R.png)

The result actually ended up solving 3 less episodes than the default reward method. This might be a hint that our issue is our learning method and not our reward. However looking at the graph it seems that this method acheived more episodes to be solved in quicker times, which is a positive outcome.

In 10,000 iterations there was 144 solved episodes.

## Monte Carlo: -1/10 Reward, 3 numbers of precision

Since we did see an improvement in the speed in which episodes where completed, I thought It'd try to see the limits of what pushing the size of the reward can do for our performance. This run I increased the reward for a positive state to be a value of 10.

![Monte Carlo](https://i.imgur.com/isPNVvc.png)

Funny enough this resulted in solving the exact same number of episodes as the run with our -1/1 reward structure. It also seems that there are less episodes being solved in faster times when compared to our -1/1 reward.

In 10,000 iterations there was 144 solved episodes.

## Monte Carlo: Default Reward, 2 numbers of precision

Just to try out different things I lowered the number of decimal places we care about when determining a state. 

![Monte Carlo](https://i.imgur.com/Dwodo3m.png)

This actually ended up solving 15 more episodes than our previous pest

In 10,000 iterations there was 162 solved episodes.

## Monte Carlo: Default Reward, 1 numbers of precision

Since it was an improvement I also tried lowering it to one signifigant digit we care about to see what the results would be. Unfortuantely it ended up decreasing in performance, so it looks as if 2 is the optimal number of digists to care about

![Monte Carlo](https://i.imgur.com/HqfrH5q.png)

In 10,000 iterations there was 157 solved episodes.

## Monte Carlo: Default Reward, 2 numbers of precision, Different Discount Factors.

Next I tried to implement a discount factor so that each reward for each state is discounted by the current time step so that reward_at_timestep = reward*(discout^timestep). A discount of 1 would end up having no discount at all, and a discount of 0 would mean that no reward is ever given. After trying this with multiple discount factors we actually ended up having an improvement with a discount of 0.8 solving 169 episodes over 10,000 iterations.

![Monte Carlo](https://i.imgur.com/UCZFhAv.png)

0.8 seems to be the sweet spot, as any more or any less seems to degrade performance.

![Monte Carlo Discount](https://i.imgur.com/97Y9JR1.png)