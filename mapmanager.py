from direct.showbase.ShowBase import ShowBase

class Mapmanager(ShowBase):
    def __init__(self, render, loader, file):
        self.loader = loader
        self.render = render
        self.land = None
        self.model = 'block.egg'
        self.texture = 'block.png'
        self.colors = [(0.2, 0.2, 0.35, 1), 
                       (1, 0, 0, 1), 
                       (0, 0, 1, 1), 
                       (0.2, 0.2, 0, 1)]
        self.load_land(file)

    def clear(self):
        if self.land:
            self.land.remove_node()
        self.startNew()

    def isEmpty(self,pos):
        blocks = self.findBlocks(pos)
        if blocks:
            return False
        return True
    
    def findBlocks(self, pos):
        return self.land.findAllMatches('=at=' + str(pos))
    
    def findHighestEmpty(self, pos):
        x, y, z = pos
        z = 1
        while not self.isEmpty((x,y,z)):
            z += 1
        return (x,y,z)

    def load_land(self, file):
        self.clear()
        file = open(file)
        file = file.readlines()
        y = 0
        for string in file:
            x= 0
            string_list = string.split(' ')
            for z  in string_list:
                for z_cor in range(int(z)):
                    self.addBlock((x, y, z_cor), self.setColor(z_cor))
                x += 1
            y += 1

    def setColor(self, z_cor):
        length = len(self.colors)
        if z_cor > length - 1:
            return self.setColor(z_cor - length)
        return self.colors[z_cor]

    
    def addBlock(self, pos, color = (0.2,0.2,0.35,1)):
        self.block = self.loader.loadModel(self.model)
        texture = self.loader.loadTexture(self.texture)
        self.block.setTexture(texture)
        self.block.setColor(color)
        self.block.setPos(pos)
        self.block.reparentTo(self.land)
        self.block.setTag('at', str(pos))
    
    def startNew(self):
        self.land = self.render.attachNewNode("Land")