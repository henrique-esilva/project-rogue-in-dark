class Map:
    map_size = (10, 10)

    player = None
    enemies=[] # mobs may have .position .health .storage
    objects=[] # objects too
    caixas=[]
    items=[]
    lightpoints={}

    def get_full_spaces(self, obj):
        v = ()
        mobs = self.enemies+self.objects+[self.player]+self.caixas
        for i in mobs:
            if i != obj:
                v += (i.position,)
        return v