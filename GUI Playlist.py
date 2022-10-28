import pygame
import webbrowser

class Video:
	def __init__(self, title, link):
		self.title = title
		self.link = link
		self.seen = False

	def open(self):
		if webbrowser.open(self.link):
			self.seen = True

class Playlist:
	def __init__(self, name, description, rating, videos):
		self.name = name
		self.description = description
		self.rating = rating
		self.videos = videos
		self.seen = False

class Playlists:
	def __init__(self, videos):
		self.videos = videos
		self.seen = False

class TextButton:
	def __init__(self, text, position,link, position2):
		self.text = text
		self.position = position
		self.link = link
		self.position2 = position2

	def is_mouse_on_text(self):
		mouse_x, mouse_y = pygame.mouse.get_pos()
		if (mouse_x > self.position[0]) and (mouse_x < self.position[0] + self.text_box[2]) and (mouse_y > self.position[1]) and (mouse_y < self.position[1] + self.text_box[3]):
			return True
		else:
			return False
	
	def draw(self): #draw playlist name and description
		font = pygame.font.SysFont('bahnschrift', 30)
		text_render = font.render(self.text, True, (0,0,0))
		self.text_box = text_render.get_rect()
		pygame.draw.rect(screen, (255,255,255), (self.position[0], self.position[1], self.text_box[2], self.text_box[3]))

		if self.is_mouse_on_text():
			text_render = font.render(self.text, True, (0,0,255))
			font2 = pygame.font.SysFont('bahnschrift', 30)
			text_render2 = font2.render(self.link, True, (0,0,0))
			self.text_box_2 = text_render2.get_rect()
			pygame.draw.line(screen, (0,0,255), (self.position[0], self.position[1] + self.text_box[3]), (self.position[0] + self.text_box[2], self.position[1] + self.text_box[3]), 2)
			pygame.draw.rect(screen, (139,139,139), (self.position2[0],self.position2[1],self.text_box_2[2],self.text_box_2[3]))
			screen.blit(text_render2, self.position2)
		else:
			text_render = font.render(self.text, True, (0,0,0))
		screen.blit(text_render, self.position)
	
	def draw_videos_btn(self): # draw playlist title and link
		font = pygame.font.SysFont('bahnschrift', 30)
		text_render = font.render(self.text, True, (0,0,0))
		self.text_box = text_render.get_rect()
		pygame.draw.rect(screen, (255,255,255), (self.position[0], self.position[1], self.text_box[2], self.text_box[3]))

		if self.is_mouse_on_text():
			text_render = font.render(self.text, True, (0,0,255))
			font2 = pygame.font.SysFont('bahnschrift', 22)
			text_render2 = font2.render(self.link, True, (0,0,0))
			self.text_box_2 = text_render2.get_rect()
			pygame.draw.line(screen, (0,0,255), (self.position[0], self.position[1] + self.text_box[3]), (self.position[0] + self.text_box[2], self.position[1] + self.text_box[3]), 2)
			pygame.draw.rect(screen, (139,139,139), (self.position2[0],self.position2[1],self.text_box_2[2],self.text_box_2[3]))
			screen.blit(text_render2, self.position2)

		else:
			text_render = font.render(self.text, True, (0,0,0))
		screen.blit(text_render, self.position)

def read_video_from_txt(file):
	title = file.readline()
	link = file.readline()
	video = Video(title,link)
	return video

def read_videos_from_txt(file):
	videos = []
	total = file.readline()
	for i in range(int(total)):
		video = read_video_from_txt(file)
		videos.append(video)
	return videos

def read_playlist_from_txt(file):
	playlist_name = file.readline()
	playlist_desc = file.readline()
	playlist_rating = file.readline()
	playlist_videos = read_videos_from_txt(file)
	playlist = Playlist(playlist_name, playlist_desc, playlist_rating, playlist_videos)
	return playlist

def read_playlists_from_txt():
	playlists = []
	with open("data.txt", "r") as file:
		total = file.readline()
		for i in range(int(total)):
			playlist = read_playlist_from_txt(file)
			playlists.append(playlist)
	return playlists

pygame.init()
screen = pygame.display.set_mode((700,500))
pygame.display.set_caption('GUI PLAYLIST')
running = True
clock = pygame.time.Clock()

# load data
playlists = read_playlists_from_txt()

videos_btn_list = []
playlists_btn_list = []
margin = 100
playlist_choice = None
for i in range(len(playlists)):
	playlist_btn = TextButton(playlists[i].name.rstrip(), (20,50+margin*i), playlists[i].description.rstrip(), (20,90+margin*i))
	playlists_btn_list.append(playlist_btn)

while running:		
	clock.tick(60)
	screen.fill((255,97,3))

	for playlist_button in playlists_btn_list:
		playlist_button.draw_videos_btn()
	for video_button in videos_btn_list:
		video_button.draw_videos_btn()

	for event in pygame.event.get():
		if event.type == pygame.MOUSEBUTTONDOWN:
			if event.button == 1:
				for i in range(len(playlists_btn_list)):
					if playlists_btn_list[i].is_mouse_on_text(): 	
						playlist_choice = i				
						videos_btn_list = []
						for j in range(len(playlists[i].videos)):
							margin1 = 80
							video_btn = TextButton(str(j+1) + ". " + playlists[i].videos[j].title.rstrip(), (275,50+margin1*j), playlists[i].videos[j].link.rstrip(), (275,90+margin1*j))
							videos_btn_list.append(video_btn)

				if playlist_choice != None:
					for i in range(len(videos_btn_list)):
						if videos_btn_list[i].is_mouse_on_text():
							playlists[playlist_choice].videos[i].open()

		if event.type == pygame.QUIT:
			running = False
				
	pygame.display.flip()

pygame.quit()