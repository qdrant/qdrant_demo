import { CSSObject, MantineThemeOverride } from "@mantine/core";
import { heights, sizing, widths } from "./sizing";

const globalStyles = (): CSSObject => {
  return {
    "#root": {
      overflow: "auto",
      display: "block",
      width: widths.screen,
      height: heights.screen,
      backgroundColor: "#F2F6FF",
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
    purple: ["#724CEF"],
    blue: ["#148BF4"],
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
  },
  headings: {
    fontFamily: "Roboto,Roboto Mono",
    sizes: {
      h1: {
        fontSize: "5rem",
        lineHeight: "6rem",
      },
      h2: {
        fontSize: "4rem",
        lineHeight: "4.75rem",
      },
      h3: {
        fontSize: "3.5rem",
        lineHeight: "4.25rem",
      },
      h4: {
        fontSize: "3rem",
        lineHeight: "3.5rem",
      },
      h5: {
        fontSize: "2.5rem",
        lineHeight: "3rem",
      },
      h6: {
        fontSize: "2rem",
        lineHeight: "2.5rem",
      },
    },
  },
  primaryColor: 'Primary',
	spacing: {
		xxs: '0.2rem',
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
        },
        P16: {
          fontSize: "1rem",
          lineHeight: "1.5rem",
        },
        P14: {
          fontSize: "0.875rem",
          lineHeight: "1.3125rem",
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
