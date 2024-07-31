import argparse

from src.agent import Agent
from src.environment import Environment


def main(flags):
    num_episodes = flags.episodes
    lr = flags.gamma
    epsilon = (flags.epsilon_low, flags.epsilon_high)
    name = flags.name
    size = flags.size

    agent = Agent(state_size=3, action_size=size ** 2, name=name, lr=lr, epsilon=epsilon)
    env = Environment(size=size)

    for episode in range(num_episodes):
        env.reset()
        state = env.get_state()['state']
        board = env.get_state()['board']
        turn = env.get_state()['turn']

        while not env.is_done():
            action, action_square = agent.act(board, state, turn)

            env.update(action_square)

            next_state = env.get_state()['state']

            agent.step(state, action, next_state)

            state = next_state

        agent.update(env.get_state()['reward'])

        if episode % 10000 == 0:
            try:
                agent.print_metrics()
            except:
                pass

    agent.save()


if __name__ == "__main__":
    # main(num_episodes=1000000, lr=0.1, epsilon=(0.01, 1.0), name='Agent1')
    # main(num_episodes=1000000, lr=0.01, epsilon=(0.01, 1.0), name='Agent2')
    # main(num_episodes=1000000, lr=0.001, epsilon=(0.01, 1.0), name='Agent3')
    # main(num_episodes=1000000, lr=0.01, epsilon=(0.5, 1.0), name='Agent4')
    # main(num_episodes=1000000, lr=0.01, epsilon=(0.001, 1.0), name='Agent5')
    # main(num_episodes=1000000, lr=0.01, epsilon=(0.9, 1.0), name='Agent6')
    # main(num_episodes=1000000, lr=0.01, epsilon=(0.001, 0.01), name='Agent7')
    # main(num_episodes=1000000, lr=0.9, epsilon=(0.01, 1.0), name='Agent8')

    parser = argparse.ArgumentParser()

    parser.add_argument('--name', type=str,
                        default="Agent",
                        help="The name of the agent")

    parser.add_argument('--episodes', type=int,
                        default=10000,
                        help="The number of episodes to complete")

    parser.add_argument('--gamma', type=float,
                        default=0.01,
                        help="The learning rate")

    parser.add_argument('--epsilon_high', type=float,
                        default=1.0,
                        help="The upper end for the exploration exploitation")

    parser.add_argument('--epsilon_low', type=float,
                        default=0.01,
                        help="The lower end for the exploration exploitation")

    parser.add_argument('--size', type=int,
                        default=3,
                        help="The size of the grid")

    flags, unparsed = parser.parse_known_args()

    main(flags)