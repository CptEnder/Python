"""
Created on Wed 23 Sep 11:04 2020
Finished on
@author: Cpt.Ender
                                  """
import Obstacle_Drawing_Board as Odb


def A_star(start_node: Odb.Node, end_node: Odb.Node):
    Open_list = []  # Nodes to be evaluated
    Closed_list = []  # Nodes that have already been evaluated
    Open_list.append(start_node)

    while Open_list:
        Board.clock.tick(10)
        Board.draw()
        current_node = Open_list[0]
        for node in Open_list:
            if node.f_cost < current_node.f_cost or \
                    (node.f_cost == current_node.f_cost and node.h_cost < current_node.h_cost):
                current_node = node
        Open_list.pop(Open_list.index(current_node))
        Closed_list.append(current_node)
        if current_node not in Board.checkedList:
            Board.checkedList.append(current_node)

        if current_node == end_node:
            Board.Retrace_Path()
            return

        for neighbor in current_node.neighbors:
            if not neighbor.traversable or neighbor in Closed_list:
                continue

            newMovement_g_Cost = current_node.g_cost + Odb.get_Distance(current_node, neighbor)
            if newMovement_g_Cost < neighbor.g_cost or neighbor not in Open_list:
                neighbor.g_cost = newMovement_g_Cost
                neighbor.update_f_Cost()
                neighbor.parent = current_node
                if neighbor not in Open_list:
                    Open_list.append(neighbor)
    print("No path found")


if __name__ == '__main__':
    Board = Odb.Board('A_Star Algorithm Visualization', [600, 600], [20, 20])

    while Board.running():
        Board.draw()
        # Board.clock.tick(20)
        Board.logig()
        if Board.Alg_running:
            Board.Alg_running = False
            A_star(Board.start_node, Board.end_node)
    Board.quit()
