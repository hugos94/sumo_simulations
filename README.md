# Sumo Simulations

-- Nodes and Edges
Para criar a rede, crie os arquivos para os nodes e os edges.

Logo apos, execute a seguinte linha de comando:

netconvert --node-files=cross.nod.xml --edge-files=cross.edg.xml --output-file=cross.net.xml

or with abbreviations

netconvert -n=cross.nod.xml -e=cross.edg.xml -o==cross.net.xml

O arquivo da rede será gerado: cross.net.xml

Para simular a rede execute a seguinte linha de comando no console:

sumo-gui -c cross.sumocfg

-- Nodes, Edges, Connections and Types

Para criar a rede, crie os arquivos para os nodes e os edges.

Logo apos, execute a seguinte linha de comando:

netconvert --node-files=MyNodes.nod.xml --edge-files=MyEdges.edg.xml --connection-files=MyConnections.con.xml --type-files=MyTypes.typ.xml --output-file=MySUMONet.net.xml

or with abbreviations

netconvert -n=MyNodes.nod.xml -e=MyEdges.edg.xml -x=MyConnections.con.xml -t=MyTypes.typ.xml -o=MySUMONet.net.xml

O arquivo da rede será gerado: cross.net.xml

Para simular a rede execute a seguinte linha de comando no console:

sumo-gui -c cross.sumocfg
