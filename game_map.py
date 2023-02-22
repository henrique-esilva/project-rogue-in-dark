class Map:
    map_size = (10, 10)

    player = None
    enemies=[] # mobs may have .position .health .storage
    objects=[] # objects too
    items=[]
    lightpoints={}

    def get_full_spaces(self, obj):
        v = ()
        mobs = self.enemies+self.objects+[self.player]
        for i in mobs:
            if i != obj:
                v += (i.position,)
        return v