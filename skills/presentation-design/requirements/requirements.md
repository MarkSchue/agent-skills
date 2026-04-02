# New card requirements
1. Create a new card. The name is given in the next "#"-section in this file.
2. The new card is a subclass of the baseclass, so it inherits all functionality and design items from the base.
3. The new card can be fully customized per css-subclass, as well as per instance in the md-file.

# stacked-text-card

1. The stacked text card has a header on top (h2-style) and a body text below (text-body style).
2. The body text is splitted in 2 to 4 text blocks.
3. header and body text can be aligned left, center or right.
4. the content should be separated by a divider line, which can be customized in color, width and thickness, or hidden completely. default is 50% width, other default styles is same as title divider line.
5. the content is vertically distributed. but be patient, when we have two cards of this style with the same number of text blocks, they should have the same distribution of text blocks, even if the content of one card is much shorter than the other. Means the seperation lines are in the same place on both cards, so they look consistent.
6. divider line can also be aligned to the left, center or right, but should be consistent across cards on the same slide.
7. it should be possible to define the vertical gaps between text blocks, and between header and first text block, and between last text block and footer.
