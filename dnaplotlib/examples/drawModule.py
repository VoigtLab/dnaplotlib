'''render module and check coordinates
need to be moved outside the example directory 
at the same directory as render.py
'''

from render import *
import matplotlib.pyplot as plt

fig, ax = plt.subplots(1, figsize=(8,10))
ax.set_xlim(XMIN, XMAX)
ax.set_ylim(YMIN, YMAX)
ax.set_axis_off()

for i, m_frame in enumerate(m_frames):
	actual_frame = draw_module(ax, design.modules[i], m_frame)
	print('desired frame: ' + str(m_frame))
	print('actual frame: ' + str(actual_frame))
	ax.scatter(actual_frame.origin[0], actual_frame.origin[1], c='red')
	ax.scatter(actual_frame.origin[0], actual_frame.origin[1] + actual_frame.height, c='red')
	ax.scatter(m_frame.origin[0], m_frame.origin[1] + m_frame.height, c='green') # mpte difference in actual frame when there is promoter
	 
plt.show()