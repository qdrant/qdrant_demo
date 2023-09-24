import { CSSObject, MantineThemeOverride } from "@mantine/core";
import { heights, sizing, widths } from "./sizing";
import { Tuple, DefaultMantineColor } from "@mantine/core";

type ExtendedCustomColors =
  | "Primary"
  | "P500"
  | "secondary"
  | "blue"  
  | "purple"
  | "teal"
  | "Neutral"
  | "N500"
  | "Error"
  | "E500"
  | "Success"
  | "S500"
  | "Warning"
  | "W500"
  | "pink"
  | DefaultMantineColor;

declare module "@mantine/core" {
  export interface MantineThemeColorsOverride {
    colors: Record<ExtendedCustomColors, Tuple<string, 10>>;
  }
}

const globalStyles = (): CSSObject => {
  return {
    "#root": {
      overflow: "auto",
      display: "block",
      width: widths.screen,
      height: heights.screen,
      backgroundColor: "#F2F6FF",
      fontFamily: "Roboto,Roboto Mono",
    },
  };
};

const myTheme: MantineThemeOverride = {
  globalStyles,
  defaultRadius: "md",
  fontFamily: "Roboto,Roboto Mono",
  colors: {
    Primary: ["#FFC2D6", "#F5587F", "#DC244C", "#A31030", "#660223"],
    P500: ["#DC244C"],
    secondary: ["#724CEF", "#148BF4", "#009999"],
    blue: [
      "#E7F5FF",
      "#D0EBFF",
      "#A5D8FF",
      "#74C0FC",
      "#4DABF7",
      "#339AF0",
      "#148BF4",
      "#228BE6",
      "#1C7ED6",
      "#1971C2",
    ],
    purple: ["#724CEF"],
    teal: ["#009999"],
    Neutral: [
      "#F2F6FF",
      "#DCE4FA",
      "#AEBDE5",
      "#8B9CCC",
      "#6A80BD",
      "#5069AD",
      "#39508F",
      "#1F3266",
      "#102252",
      "#06153D",
    ],
    N500: ["5069AD"],
    Error: ["#FED6D6", "#F03030", "#661414"],
    E500: ["#F03030"],
    Success: ["#D1FADF", "#12B765", "#085232"],
    S500: ["#12B765"],
    Warning: ["#FEE4C7", "#F5870A", "#662F0A"],
    W500: ["#F5870A"], 
    pink: [
      "#FFF0F6",
      "#FFDEEB",
      "#FCC2D7",
      "#FAA2C1",
      "#F783AC",
      "#F06595",
      "#DC244C",
      "#D6336C",
      "#C2255C",
      "#A61E4D",
    ],
  },
  primaryColor: "Primary",
  spacing: {
    xxs: "0.2rem",
  },
  other: {
    sizing,
    heights,
    widths,
    fontWeights: {
      thin: 100,
      extraLight: 200,
      light: 300,
      normal: 400,
      medium: 500,
      semibold: 600,
      bold: 700,
      extrabold: 800,
      black: 900,
    },
    subheading: {
      sizes: {
        SH18: {
          fontSize: "1.125rem",
          lineHeight: "1.5rem",
        },
        SH12: {
          fontSize: "0.75rem",
          lineHeight: "1.125rem",
        },
      },
    },
    paragraph: {
      sizes: {
        P24: {
          fontSize: "1.5rem",
          lineHeight: "2rem",
        },
        P18: {
          fontSize: "1.125rem",
          lineHeight: "1.6875rem",
          fontWeight: 400,
        },
        P16: {
          fontSize: "1rem",
          lineHeight: "1.5rem",
        },
        P14: {
          fontSize: "0.875rem",
          lineHeight: "1.3125rem",
          fontWeight: 400,
        },
        P12: {
          fontSize: "0.75rem",
          lineHeight: "1.125rem",
        },
      },
    },
  },
};

export default myTheme;
