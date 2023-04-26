class Map:
    map_size = (10, 10)

    player = None
    enemies=[] # mobs may have .position .health .storage
    objects=[] # objects too
    caixas=[]
    items=[]
    paredes=[
        #paredes retas
        [(1,0),(2,0),(3,0),(4,0),(5,0),(6,0),(7,0),(8,0),(9,0),(10,0),(11,0)],
        [(0,1),(0,2),(0,3),(0,4)],
        [(1,5),(2,5),(3,5),(4,5),(5,5)],
        [(6,4),(6,3),(6,2),(6,1)],
        #paredes esquina
        [(0,0)],
        [(0,5)],
        [(6,5)],
        [(6,0)]
    ]
    floors=[
        ((1,1),(5,4))
    ]
    lightpoints={}

    def get_full_spaces(self, obj):
        v = ()
        mobs = self.enemies+self.objects+[self.player]+self.caixas
        for i in mobs:
            if i != obj:
                v += (i.position,)
        return v