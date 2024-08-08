import argparse
import time
from agents import Agent
from environment import Environment

import socket

def main(flags):
    num_episodes = flags.episodes
    lr = flags.gamma
    epsilon = (flags.epsilon_low, flags.epsilon_high)
    name = flags.name
    agent = Agent(name=name, lr=lr, epsilon=epsilon)
    env = Environment()

    for episode in range(num_episodes):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(("pyctf.class.net", 8086))
        env.reset()
        env.update(s.recv(2048))
        state = env.get_state()['state']
        board = env.get_state()['board']
        block = env.get_state()['block']
        offset = env.get_state()['offset']

        while not env.done:
                action = agent.act(board, block, offset)
                s.send(f'{action['op']}\n'.encode())
                time.sleep(.05)
                res = s.recv(2048)
                env.update(res)

                next_state = env.get_state()['state']

                agent.step(state, action, next_state)

                state = env.get_state()['state']
                board = env.get_state()['board']
                block = env.get_state()['block']
                offset = env.get_state()['offset']

        agent.update(env.get_state()['reward'])
        print(f"Finished Episode: {episode} with a reward of: {env.get_state()['reward']}")
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
                        default=0.001,
                        help="The learning rate")

    parser.add_argument('--epsilon_high', type=float,
                        default=1.0,
                        help="The upper end for the exploration exploitation")

    parser.add_argument('--epsilon_low', type=float,
                        default=0.001,
                        help="The lower end for the exploration exploitation")
    
    flags, unparsed = parser.parse_known_args()

    main(flags)