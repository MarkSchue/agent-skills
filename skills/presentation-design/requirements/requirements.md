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
### Common card properties -> baseclass
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
    9. The baseclass should also be enhanceable with new properties if needed. If we need to add new properties to the design system, we should be able to easily add them to the base class without breaking existing slides.

### Specific card properties -> subclasses
10. For specific card types, we can define additional properties that are relevant to that type of content. For example, for a `KPI-card`, we might want to define properties for text alignment, font size, and color specific to the KPI values. Similarly, for an `ImageCard`, we might want to define properties for image source, image size, and image alignment. This approach allows us to have a clear and organized structure for our card definitions, while also allowing for flexibility and customization for different types of content.

# Agenda
1. Based on the sections defined in the presentation definition md-file, we should be able to automatically generate an agenda slide that lists the main sections of the presentation. The agenda slide should follow the same design theme and layout as the other slides, and should be easily customizable via the design tokens in the css class. The agenda slide should also be able to handle a variable number of sections, and should automatically adjust the layout and spacing to accommodate the content.
2. The agenda should be automatically gemerated only once (!) at the beginning of the md-file, and then injected in the presentation at the positions where the sections change. For example, if we have three sections in the presentation, we should have three agenda slides that are automatically generated and injected at the appropriate positions in the presentation. This allows for easy navigation and a clear overview of the presentation structure for the audience.

# Renderer Notes
1. The renderer should be able to parse the presentation definition in the md-file and generate the corresponding slides based on the defined layouts and card types. The renderer should also be able to apply the design tokens defined in the css class to ensure consistent styling across the presentation. The renderer should also be  able to handle any overrides defined in the md-file for specific instances of slides or cards, allowing for flexibility while maintaining a consistent design language across the presentation. The renderer should also be able to handle any new properties added to the design system in the future without breaking existing slides.
2. The renderer should also be able to export the generated slides in a format that can be easily shared and presented, such as a PowerPoint file or draw.io file. The exported slides should maintain the design and layout defined in the presentation definition, while also being compatible with common presentation software. The renderer should also be able to handle any media content included in the cards, such as images or charts, and ensure that they are properly displayed in the exported slides.
3. When we add a < !-- DONE --> comment below the "##" slide title, never touch and change this slide. maybe the user has already exported this slide and we don't want to break it by changing the layout or design tokens. This allows for a clear separation between slides that are still in development and those that are finalized and should not be modified. The renderer should respect this convention and ensure that any slides marked with the < !-- DONE --> comment are not altered during the rendering process.


# Skill definition
1. Define a clear skill defintion of what the skill is and what it does. This should be stored in a skill.md-file.
2. Every card that is available and every layout that is available should be clearly integrated into a YAML-file, that acts as a registry for the skill. maybe in the future i ask you to create a new presentation. based on the card definitions (name, keyword, purpose) you should be able to identifiy which card to use. this should also prevent reading the complete md-files for each card to minimize the content-size of the chat. First read the yaml-file to get an overview of the available cards and layouts, and then only read the md-files for the specific cards and layouts that are needed for the presentation. This allows for efficient use of resources while still providing access to the necessary information for creating the presentation.
3. Try to create as much logic inside python scripts as possible, to be as deterministic as possible. The md-file should be rendered into a presentation only by using the python scripts, which should be able to handle all the logic for parsing the md-file, applying the design tokens, and generating the slides. This allows for a clear separation between the content definition (in the md-file) and the rendering logic (in the python scripts), making it easier to maintain and update both components in the future. The python scripts should also be designed to be flexible and adaptable to any changes in the design system or presentation definition, allowing for easy updates and improvements over time.
4. Set up a very good approach for classes and inheritance in the python scripts, to ensure that we can easily add new card types and layouts in the future without breaking existing functionality. The classes should be designed to be modular and reusable, allowing for easy extension and customization as needed. The inheritance structure should also be clear and well-documented, making it easy for other developers to understand and contribute to the codebase in the future. This approach will help ensure that the skill remains maintainable and scalable as it evolves over time.
5. Create one virtual environment for python within the skill folder and refer to only this venv. This should prevent any issiues with dependencies and the creation of new venvs for each project. By using a single virtual environment for the skill, we can ensure that all dependencies are properly managed and that there are no conflicts between different projects. This also allows for easier maintenance and updates to the dependencies, as we only need to manage them in one place. The virtual environment should be clearly documented and included in the skill repository, making it easy for other developers to set up and use when working on the skill.
6. in the skill folder there should be a clear structure for organizing the different components of the skill, such as the md-files for the presentation definition and card documentation, the css-file for the design tokens and layout definitions, and the python scripts for rendering the presentation. This structure should be well-documented and easy to navigate, allowing for efficient development and collaboration on the skill. The organization of the skill folder should also allow for easy expansion in the future, as new card types, layouts, or design tokens are added to the skill. This will help ensure that the skill remains maintainable and scalable as it evolves over time.

# Additional requirements
1. I need a functionality to scaffold a new presentation with a predefined folder structure, including the md-file for the presentation definition, the css-file for the design tokens and layout definitions, and the python scripts for rendering the presentation. This scaffolding functionality should be easy to use and should generate all the necessary files and folders for a new presentation, allowing me to quickly get started on creating a new presentation without having to set up the structure manually each time. The scaffolding functionality should also include clear documentation on how to use it and how to customize the generated files for my specific presentation needs. This will help streamline the process of creating new presentations and ensure that I can focus on the content and design rather than the setup.
2. Folder should be:
  - presentation-name/
    - presentation-definition.md
    - theme.css
    - output/
      - presentation.pptx
      - presentation.drawio
    - assets/
      - images/
      - charts/
      - diagrams/
      - logos/
3. the css-file should be a copy of the skill-level css-file, where I can then customize the design tokens and layout definitions for my specific presentation. This allows me to maintain a consistent design language across my presentations while also allowing for customization as needed. The css-file should be well-documented, with clear explanations of each design token and layout definition, making it easy for me to understand and modify the styles for my presentation. This will help ensure that I can create visually appealing and cohesive presentations that align with my desired design aesthetic.
