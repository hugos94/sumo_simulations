Para criar a rede, crie os arquivos para os nodes e os edges.

Logo apos, execute a seguinte linha de comando:

netconvert --node-files=cross.nod.xml --edge-files=cross.edg.xml --output-file=cross.net.xml

O arquivo da rede será gerado: cross.net.xml

Para simular a rede execute a seguinte linha de comando no console:

sumo-gui -c cross.sumocfg
