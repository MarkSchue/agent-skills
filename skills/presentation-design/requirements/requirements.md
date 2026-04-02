# Objective
I would like to set up a new skill for designing presentation. The approach should be to have a lean set of flexible, reusable components that can be assembled into a wide variety of slide layouts. The skill should be based on card-based design system principles, with a clear definition of cards and layouts for slides. The skill should also include a token system for consistent styling and easy theming.
# Requirements

## Design theme
1. The design system should be based on a card-based design system, where each card is a self-contained unit of content that can be easily reused and rearranged across slides.
2. The design theme should include a set of design tokens for colors, typography (fonts), borderstyles, shadows etc. This global definition of the design system should go in one class with subclasses if needed. In the future I will ask you to investigate a pptx or website and extract the design tokens from it to populate the theme.

## Presentation definition
1. The presentation definition should be in a very structured format as md-file.
    - Each new section begins with "#" which also becomes an entry in our agenda system
    - Each slide begins with a "##" which becomes the slide title
    - Each card on the slide begins with a "###" which becomes the card title
    - Each card contains a YAML code block with the card type and its content and styling properties
2. The presentation definition should be easy to read and write for humans, while also being easily parseable by the agent. The YAML code blocks should follow a consistent schema for each card type, with clear definitions of required and optional fields.
3. For the cards, we need one md-file per card, where the card is documented. there should be a character-based piktogram at the top of the md-file, that clearly describes the card layout and the position of the different elements. The card md-file should also include a detailed description of the card, its parameters, and the design tokens it uses.

## Slide Layouts
1. The slide layout should be defined in a css-file. Every propertiy that defines the slide layout (fontsize, title font color, title font size, title line color, title line width, title line alignment, title alignment, card padding, card border radius, card border color, card background color) should be defined as a token in the css file within that css-class. Everything that defines the layout and the theming of the slides should be included in this class. This allows for easy theming and consistent styling across slides.
1. The slide layout system should support a range of common presentation formats, including:
   - Title slide
   - Layouts in the format (rows x columns). we should have a set of predefined configurations with up to three rows and four columns.
   - A clear definition about the canvas size for the slides. Standard should be 16:9
   - A clear defintiion of the margin top and right.
   - A clear definition of the margin between the cards.
   - Any possible background color or even bqackground images should be defined in the css file as well in this class.
2. The slide layout should support following elements, which can be customized via the design tokens in the css class. For each element we should be able to define the fontsize, font color, font weight, background color, border color, border width, border radius, padding and margin, position, width, height, alignment, and any other relevant properties:
   - Slide title
   - Slide subtitle
   - Title line (divider below the title)
   - Primary logo (top right by default)
   - Secondary logo (top left by default)
   - Footer line (divider above the footer)
   - Footer text (bottom right by default)
   - Page number (bottom left by default)
3. The csc-class should be enhanceable with new properties if needed. If we need to add new properties to the design system, we should be able to easily add them to the css class without breaking existing slides.
4. The so created css-class is then valid for all slides. For each slide we can then override the properties defined in the css class with slide-specific values if needed. This allows for flexibility while maintaining a consistent design language across the presentation.

## Card layouts
1. The cards follow a common approach, means we have a set of propertynames each card-type follows. this allows us to have a consistent way of defining the styles of the cards and also allows us to easily add new card types in the future. For each card type we should have a clear definition of the required and optional properties, as well as the design tokens that can be used to customize the appearance of the card.
2. As already described for the slides, we would like to have one common base class (python class as well as css-class), where cards are defined.
3. Beside the common baseclass, we then define special classes which inherit from the baseclass and add specific properties for the different card types. For example, we could have a `TextCard` class that inherits from the base `Card` class and adds properties for text content, font size, and text color. We could also have a `ImageCard` class that adds properties for image source, image size, and image alignment. This approach allows us to have a clear and organized structure for our card definitions, while also allowing for flexibility and customization for different types of content. This approach should be reflected in the css-file, where parameters that are common to all cards are defined in a base class, and specific parameters for different card types are defined in subclasses. Just remember, that for specific instances of cards we can override the properties defined in the css class with card-specific values if needed in the md-file. This allows for flexibility while maintaining a consistent design language across the presentation.
4. The card has a "title" which sits on top of the card and is separated from the body. The title can optionally be hidden. Alignment left, center, right is possible. defualt is left and defined in the css-baseclass.

5. The title is divided by the "header line" (divider below the title). The header line can optionally be hidden. The color, width and alignment of the header line can be defined in the css-baseclass and can be overridden in the md-file for specific instances of cards.
6. The body of the card can contain different types of content, such as text, images, or charts. The body should be flexible enough to accommodate different types of content while maintaining a consistent design language across the presentation. The body should also be customizable via the design tokens in the css class, allowing for easy theming and consistent styling across slides.
7. For the body, we define predefined styles for text (including fontsize, color, backgroundcolor, italic, bold, etc):
    - Heading 1
    - Heading 2
    - Body text
    - Caption text
    - Label text
    - Quote text
    - Footnote text
8. For the body, we also define predefined styles for images (including size, alignment, border color, border width, border radius, etc):
    - Full bleed image
    - Framed image
    - Circular image


