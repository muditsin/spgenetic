
MIN_VERTEX_COUNT = 10
MAX_VERTEX_COUNT = 101
CELL_PREFIX = 'cell'
CELL_SEP = '_'

def index():
    size_onchange = "ajax('" + URL(r=request, f='drawTable') + "',['size'],'graph_table');"
    size = SELECT(_name='size', _value='10', value='10', _id='size', _class='integer',
                  requires=IS_INT_IN_RANGE(MIN_VERTEX_COUNT, MAX_VERTEX_COUNT),
                  _onchange=size_onchange, *range(MIN_VERTEX_COUNT, MAX_VERTEX_COUNT, 1))

    oriented = SELECT(True, False, _name='oriented', _id='oriented',
                      requires=IS_IN_SET([True, False]))

    connectivity = INPUT(_type='text', _name='connectivity', _id='connectivity',
                         _size='2', requires=IS_FLOAT_IN_RANGE(0, 1), value='0.5')

    fill_onclick = "ajax('" + URL(r=request, f='drawFilledTable') + \
                    "',['oriented','connectivity','size','max_length'],'graph_table');"
    fill_button = INPUT(_type='button', _value='Fill graph', _onclick=fill_onclick)
    max_length = INPUT(_type='text', _name='max_length', _id='max_length', _size=3,
                       requires=IS_INT_IN_RANGE(0, 10 ** 10),
                       value=100)
    form = FORM(TABLE(TR('Size', size),
                      TR('Cost', DIV(makeTable(), _id='graph_table')),
                      TR('Oriented', oriented),
                      TR('Connectivity [0,1]', connectivity),
                      TR('Max Length', max_length),
                      TR('', fill_button),
                      TR('', INPUT(_type='submit', _value='Submit'))))

    if form.accepts(request.vars, session):
        graph = makeGraphDictFromVars(int(request.vars.size), request.vars)
        session.vars = dict()
        session.vars['graph'] = graph
        session.vars['size'] = int(request.vars.size)
        redirect(URL(r=request, f='options'))

    return dict(form=form)

def options():
    from gluon.sqlhtml import form_factory
    start_vertex = SQLField('start_vertex', 'integer', default=0,
                            requires=IS_IN_SET(range(0, session.vars['size'])))
    stop_vertex = SQLField('stop_vertex', 'integer', default=session.vars['size'] - 1,
                           requires=IS_IN_SET(range(0, session.vars['size'])))
    init_pop_length = SQLField('init_population_length', 'integer', default=1000,
                               requires=IS_INT_IN_RANGE(0, 10 ** 10))
    genes_count = SQLField('genes_count', 'integer', default=10,
                           requires=IS_INT_IN_RANGE(0, 10 ** 10))
    population_count = SQLField('population_count', 'integer', default=300,
                                requires=IS_INT_IN_RANGE(0, 10 ** 10))
    child_cull = SQLField('child_cull', 'integer', default=200,
                          requires=IS_INT_IN_RANGE(0, 10 ** 10))
    child_count = SQLField('child_count', 'integer', default=1000,
                           requires=IS_INT_IN_RANGE(0, 10 ** 10))
    good_parents = SQLField('good_parents', 'integer', default=10,
                            requires=IS_INT_IN_RANGE(0, 10 ** 10))
    mutants = SQLField('mutants', 'double', default=0.1,
                       requires=IS_FLOAT_IN_RANGE(0, 1))
    form = form_factory(start_vertex,
                        stop_vertex,
                        init_pop_length,
                        genes_count,
                        population_count,
                        child_cull,
                        child_count,
                        good_parents,
                        mutants)

    if form.accepts(request.vars, session):
        session.vars['start_vertex'] = int(request.vars.start_vertex)
        session.vars['stop_vertex'] = int(request.vars.stop_vertex)
        session.vars['init_population_length'] = int(request.vars.init_population_length)
        session.vars['genes_count'] = int(request.vars.genes_count)
        session.vars['population_count'] = int(request.vars.population_count)
        session.vars['child_cull'] = int(request.vars.child_cull)
        session.vars['child_count'] = int(request.vars.child_count)
        session.vars['good_parents'] = int(request.vars.good_parents)
        session.vars['mutants'] = float(request.vars.mutants)
        redirect(URL(r=request, f='end'))
    return dict(form=form)


def end():
    go_onclick = "var btn = document.getElementById('gobtn'); btn.value='Wait please';" + \
                 "btn.disabled = 'true';" + \
                 "ajax('" + \
                    URL(r=request, f='go') + \
                    "',[],'result');"
    dej_onclick = "var dejbtn = document.getElementById('dejbtn'); dejbtn.value='Wait please';" + \
                 "dejbtn.disabled = 'true';" + \
                 "ajax('" + \
                    URL(r=request, f='dejkstra') + \
                    "',[],'dejkstra_result');"
    form = FORM(TABLE(TR('Genetic solution',
                         INPUT(_id='gobtn' , _type='button', _value='RUN', _onclick=go_onclick)),
                      TR('', DIV(_id='result')),
                      TR('Dejkstra solution',
                         INPUT(_id='dejbtn', _type='button', _value='RUN', _onclick=dej_onclick)),
                      TR('', DIV(_id='dejkstra_result'))))
    return dict(form=form)

def dejkstra():
    from applications.shortestpath.modules.shortestpath.graph import Graph
    g = Graph(session.vars['graph'])
    result = g.findShortestPathDijkstra(session.vars['start_vertex'],
                                        session.vars['stop_vertex'])
    return TABLE(TR(str(result) + ' ' + str(g.pathCost(result)))).xml()

def go():
    from applications.shortestpath.modules.shortestpath.graph import Graph
    from applications.shortestpath.modules.shortestpath.spsolution import SPSolution
    sps = SPSolution(Graph(session.vars['graph']), session.vars['start_vertex'],
                     session.vars['stop_vertex'],
                     initPopulationLength=session.vars['init_population_length'],
                     genesCount=session.vars['genes_count'],
                     populationCount=session.vars['population_count'],
                     childCull=session.vars['child_cull'],
                     childCount=session.vars['child_count'],
                     goodParents=session.vars['good_parents'],
                     mutants=session.vars['mutants'])
    results = [str(i) + ' ' + str(i.fitness()) for i in sps.bestIterator()]
    return TABLE(*[TR(r) for r in results]).xml()

def drawFilledTable():
    try:
        numVertex = int(request.vars.size)
        connectivity = float(request.vars.connectivity)
        oriented = eval(request.vars.oriented)
        maxLength = int(request.vars.max_length)
        return makeTable(fill=True, numVertex=numVertex, maxLength=maxLength,
                         connectivity=connectivity, oriented=oriented).xml()
    except ValueError:
        return makeTable().xml()

def makeGraphDictFromVars(size, vars):
    gd = {}
    for i in range(size):
        gd[i] = {}
        for k in range(size):
            value = vars[CELL_PREFIX + CELL_SEP + str(i) + CELL_SEP + str(k)]
            gd[i][k] = int(value) if value != '' else float('inf')
    return gd

def makeTable(fill=False, numVertex=10, connectivity=0.5, oriented=False, maxLength=100):
    from applications.shortestpath.modules.shortestpath.graph import Graph, generateRandomGraph
    graph = generateRandomGraph(numVertex, connectivity=connectivity,
                                maxLength=maxLength, oriented=oriented) \
            if fill else None
    trs = [TR('', *[x for x in range(numVertex)])]
    for i in range(numVertex):
        tds = []
        for k in range(numVertex):
            v = ''
            if fill:
                v = graph[i][k] if graph[i][k] != float('inf') else ''
            tds.append(INPUT(_type='text', _class='integer',
                             _name=CELL_PREFIX + CELL_SEP + str(i) + CELL_SEP + str(k), _size='1',
                             requires=IS_NULL_OR(IS_INT_IN_RANGE(0, 10 ** 10)),
                             value=v))
        trs.append(TR(i, *tds))
    return TABLE(*trs)

def drawTable():
    return makeTable(numVertex=int(request.vars.size)).xml()
