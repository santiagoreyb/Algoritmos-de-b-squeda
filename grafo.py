import heapq
class Vertex:
    def __init__(self, node):
        self.id = node
        self.adjacent = {}
      
    def __str__(self):
        return str(self.id) + ' adjacentes: ' + str([x.id for x in self.adjacent])

    def add_neighbor(self, neighbor, weight=0):
        self.adjacent[neighbor] = weight

    def get_connections(self):
        return self.adjacent.keys()

    def get_id(self):
        return self.id

    def get_weight(self, neighbor):
        return self.adjacent[neighbor]


class Graph:
    def __init__(self):
        self.vert_dict = {}
        self.num_vertices = 0

    def __iter__(self):
        return iter(self.vert_dict.values())

    def add_vertex(self, node):
        self.num_vertices = self.num_vertices + 1
        new_vertex = Vertex(node)
        self.vert_dict[node] = new_vertex
        return new_vertex

    def get_vertex(self, n):
        if n in self.vert_dict:
            return self.vert_dict[n]
        else:
            return None

    def add_edge(self, frm, to, cost=0):
        if frm not in self.vert_dict:
            self.add_vertex(frm)
        if to not in self.vert_dict:
            self.add_vertex(to)

        self.vert_dict[frm].add_neighbor(self.vert_dict[to], cost)
        self.vert_dict[to].add_neighbor(self.vert_dict[frm], cost)

    def get_vertices(self):
        return self.vert_dict.keys()

    # función heurística
    def heuristica_simple(self, nodo_objetivo):
      nodo_objetivo = self.vert_dict[nodo_objetivo]
      heuristica_simple = {}
      for nodo_id in self.vert_dict:
          nodo_actual = self.vert_dict[nodo_id]
          heuristica = abs(ord(nodo_actual.id) - ord(nodo_objetivo.id))
          heuristica_simple[nodo_id] = heuristica
      return heuristica_simple

  #BUSQUEDA EN PROFUNDIDAD
    def busqueda_profundidad(self, orig, dest):
        agenda, expand = [], []
        actual = Vertex
        expand.append(orig)
        agenda.append(orig)
        actual = self.vert_dict[orig]
        exito_ruta=False
        while agenda != [] and actual.get_id() != dest:
            actual = self.vert_dict[agenda.pop()]
            if actual.get_id()==dest:
                exito_ruta=True
            if actual.get_id() not in expand:
                expand.append(actual.get_id())
            if actual.get_connections():
                for w in actual.get_connections():
                    vid = actual.get_id()
                    wid = w.get_id()
                    if wid not in expand:
                        agenda.append(wid)
        if exito_ruta:
            print("\n")
            print("\nRECORRIDO EN PROFUNDIDAD DEL NODO: " + orig + " CON DESTINO: " + dest + "\n")
            n = len(expand)
            i = 1
            costo_tot=0
            for w in expand:
                if i < n:
                    next_index = expand.index(w)
                    next_element = expand[next_index + 1]
                    vert_actual = self.vert_dict[w]
                    vert_sig = self.vert_dict[next_element]
                    costo = vert_actual.get_weight(vert_sig)
                    costo_tot=costo_tot+costo
                    print(w + " ---> " + next_element + "  Costo: " + str(costo))
                    i += 1
                else:
                    print("\n\nCOSTO DEL RECORRIDO:"+str(costo_tot))
        else:
            print("No se econtro ruta")

        return

    def primero_anchura(self, nodo_inicio, nodo_final):
        print("\nRECORRIDO EN ANCHURA DEL NODO: " + nodo_inicio + " CON DESTINO: " + nodo_final + "\n")

        # busca el vertice con la id y la convierte  en el vertice
        nodo_inicio = self.vert_dict[nodo_inicio]

        # Creamos una lista llamada 'recorridos' para llevar un registro de los vértices ya encontrados.
        recorridos = [nodo_inicio.id]
        ruta = False
        costo = 0
        indice = 0  # auxiliar para poner las conexiones
        conec = []  # tiene las conexiones directas

        for actual in recorridos:
            indice += 1

            actual = self.vert_dict[actual]
            for w in actual.get_connections():
                wid = w.get_id()

                if w.get_id() not in recorridos:
                    recorridos.append(w.get_id())
                    conec.append(recorridos[indice - 1] + wid)  # conexion de nodo origen y su vecino

                if nodo_final in recorridos:
                    ruta = True
                    break

            if nodo_final in recorridos:
                ruta = True
                break

        recorrido = []
        recorrrido_imprim=[]
        # revisar las conexiones
        nod_conec = nodo_final
        for elemento in reversed(conec):
            if elemento.endswith(nod_conec):
                recorrido.append(nod_conec)
                #escogemos los elementos por separado  
                costo += self.vert_dict[elemento[:1]].get_weight(self.vert_dict[elemento[1:]])
                nod_conec = elemento[:1]
                #y organizar la impresion
                recorrrido_imprim.append(elemento)
        recorrido.append(nodo_inicio.id)

        
        for elemento in reversed(recorrrido_imprim):
            costo_conec= self.vert_dict[elemento[0]].get_weight(self.vert_dict[elemento[1]])
            print(str(elemento[0]) +"--->"+str(elemento[1]) +"  Costo: "+str(costo_conec)) 
        
        if ruta:
            print("\n\nCOSTO DEL RECORRIDO: " + str(costo) + "\n")
        else:
            print("\n\nNO SE ENCONTRO LA RUTA\n")

        return

    def a_estrella(self, nodo_inicial, nodo_final):
      agenda = [(0, nodo_inicial)]
      visitados = set()
      padres = {}
      costo = {nodo_inicial: 0}
  
      
  
      while agenda:
          _, actual = heapq.heappop(agenda)
  
         
  
          if actual == nodo_final:
              # Construir el camino desde el nodo de inicio hasta el nodo final
              camino = self.construir_camino(padres, nodo_inicial, nodo_final)
              print(f"Recorrido final: {' -> '.join(map(str, camino))} (Costo total: {costo[nodo_final]})")
              return
  
          if actual in visitados:
              continue
  
          visitados.add(actual)
  
          for siguiente in self.vert_dict[actual].get_connections():
              costo_actual = costo[actual] + self.vert_dict[actual].get_weight(siguiente)
              hn = self.heuristica_simple(nodo_final)[siguiente.get_id()]  # Usa el ID para obtener la heurística
  
              if siguiente.get_id() not in costo or costo_actual < costo[siguiente.get_id()]:
                  costo[siguiente.get_id()] = costo_actual
                  f_actual = costo_actual + hn
                  heapq.heappush(agenda, (f_actual, siguiente.get_id()))
                  padres[siguiente.get_id()] = actual
  
      # Si no se encuentra un camino, retornar None
      print("No se encontró un camino.")

    def construir_camino(self, padres, nodo_inicial, nodo_final):
        camino = [nodo_final]
        actual = nodo_final

        while actual != nodo_inicial:
            actual = padres[actual]
            camino.append(actual)

        camino.reverse()
        return camino

  
#------------------------------------------------------------
#------------------------------------------------------------
#------------------------------------------------------------

if __name__ == '__main__':
    g = Graph()

    op = int(1)
    print("Seleccione el grafo\n1)Grafo pequeño\n2)Grafo visto en clase")
    op = int(input("Opcion:"))
    if op==1:
        
        g.add_vertex('a')
        g.add_vertex('b')
        g.add_vertex('c')
        g.add_vertex('d')
        g.add_vertex('e')
        g.add_vertex('f')

        g.add_edge('a', 'b', 7)
        g.add_edge('a', 'c', 9)
        g.add_edge('a', 'f', 14)
        g.add_edge('b', 'c', 10)
        g.add_edge('b', 'd', 15)
        g.add_edge('c', 'd', 11)
        g.add_edge('c', 'f', 2)
        g.add_edge('d', 'e', 6)
        g.add_edge('e', 'f', 9)
    else:   
        g.add_vertex('a')
        g.add_vertex('b')
        g.add_vertex('c')
        g.add_vertex('d')
        g.add_vertex('e')
        g.add_vertex('f')
        g.add_vertex('g')
        g.add_vertex('h')
        g.add_vertex('i')
        g.add_vertex('j')
        g.add_vertex('k')
        g.add_vertex('l')
        g.add_vertex('m')

        g.add_edge('a', 'b', 10)
        g.add_edge('a', 'j', 10)    
        g.add_edge('b', 'g', 10)
        g.add_edge('b', 'c', 10)
        g.add_edge('j', 'c', 10)     
        g.add_edge('j', 'k', 10)  
        g.add_edge('g', 'h', 10)    
        g.add_edge('c', 'h', 10)    
        g.add_edge('c', 'd', 10)    
        g.add_edge('k', 'd', 10)
        g.add_edge('k', 'l', 10)
        g.add_edge('h', 'i', 10)
        g.add_edge('d', 'e', 10)
        g.add_edge('d', 'l', 10)
        g.add_edge('l', 'e', 10)
        g.add_edge('l', 'm', 10)
        g.add_edge('m', 'e', 10)
        g.add_edge('i', 'e', 10)
        g.add_edge('e', 'f', 10)
        g.add_edge('i', 'f', 10)

    for v in g:
        for w in v.get_connections():
            vid = v.get_id()
            wid = w.get_id()
            print('( %s , %s, %3d)' % (vid, wid, v.get_weight(w)))

    for v in g:
        print('g.vert_dict[%s]=%s' % (v.get_id(), g.vert_dict[v.get_id()]))
    
  
    while op != 0:
      print("\n1)Busqueda en profundidad\n2)Primero en anchura \n3)Funcion heuristica \n4)A* \n0)Salir")
      op = int(input("Opcion:"))
      match op:
        case 0:
          print("FIN")
        case 1:
          print("Algoritmo profundidad:")
          print("Origen:")
          orig=input()
          print("Destino:")
          dest=input()
          g.busqueda_profundidad(orig,dest)
        case 2:
          print("Primero en anchura:")
          print("Origen:")
          orig=input()
          print("Destino:")
          dest=input()
          g.primero_anchura(orig,dest)
        case 3:
          print("Destino:")
          nodo_objetivo=input()
          valores_heuristicas = g.heuristica_simple(nodo_objetivo)
          print("Heurísticas:")
          for nodo_id, heuristica in valores_heuristicas.items():
            print(f"Nodo {nodo_id}: {heuristica}")
        case 4:
          print("A*:")
          print("Origen:")
          inicio=input()
          print("Destino:")
          destino=input()
          g.a_estrella(inicio, destino)

          

