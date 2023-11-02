class Map:
    map_size = (10, 10)

    player = None
    enemies=[] # mobs may have __baseStats__
    objects={ # objects too
        "#door": [],
        "#lamp": [],
        "#desk": [],
    }
    caixas=[]
    items=[]
    paredes=[
        #paredes retas
        [(1,0),(2,0),(3,0),(4,0),(5,0),(8,0),(9,0)],
        [(0,1),(0,2),(0,3),(0,4),(7,1),(7,5),(7,6)],
        [(1,5),(2,5),(3,5),(4,5),(5,5)],
        [(6,1),(10,1),(10,2)],
        #paredes esquina
        [(0,0),(7,0)],
        [(0,5)],
        [(6,5)],
        [(6,0),(10,0)],
        #paredes convexas
        [(7,2)],
        [(7,4)],
        [(6,4)],
        [(6,2)],
    ]
    obstacles=[] # deprecated?
    floors=[
        ((6,3),(7,3)),
        ((1,1),(5,4)),
        ((8,1),(9,9))
    ]
    lightpoints={}

    def get_all_objects(self):
        b=[]
        for i in self.objects.values():
            b=b+i
        return b

    def get_full_spaces(self, obj):
        v = ()
        a=[]
        for i in range(len(self.paredes)):
            a=a+self.paredes[i].copy()
        b=self.get_all_objects()
        mobs = self.enemies+b+[self.player]+self.caixas+a+self.obstacles
        for i in mobs:
            if i != obj:
                try:
                    if not hasattr(i, 'intangible') or not getattr(i, 'intangible'):
                        v += (i.position,)
                except AttributeError:
                    if type(i)==type(tuple()):
                        v += (i,)
        return v