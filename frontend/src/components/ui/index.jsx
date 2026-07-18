import React from "react";
import "./ui.css";

export const Card = ({ children, className = "", ...props }) => {
  return (
    <div className={`ui-card ${className}`} {...props}>
      {children}
    </div>
  );
};

export const CardHeader = ({ children, className = "", ...props }) => {
  return (
    <div className={`ui-card-header ${className}`} {...props}>
      {children}
    </div>
  );
};

export const CardTitle = ({ children, className = "", ...props }) => {
  return (
    <h3 className={`ui-card-title ${className}`} {...props}>
      {children}
    </h3>
  );
};

export const CardContent = ({ children, className = "", ...props }) => {
  return (
    <div className={`ui-card-content ${className}`} {...props}>
      {children}
    </div>
  );
};

export const Input = React.forwardRef(({ className = "", ...props }, ref) => {
  return (
    <input
      className={`ui-input ${className}`}
      ref={ref}
      {...props}
    />
  );
});
Input.displayName = "Input";

export const Textarea = React.forwardRef(({ className = "", ...props }, ref) => {
  return (
    <textarea
      className={`ui-textarea ${className}`}
      ref={ref}
      {...props}
    />
  );
});
Textarea.displayName = "Textarea";

export const Button = React.forwardRef(({ className = "", variant = "primary", ...props }, ref) => {
  return (
    <button
      className={`ui-button ui-button-${variant} ${className}`}
      ref={ref}
      {...props}
    />
  );
});
Button.displayName = "Button";

export const Label = React.forwardRef(({ className = "", children, ...props }, ref) => {
  return (
    <label
      className={`ui-label ${className}`}
      ref={ref}
      {...props}
    >
      {children}
    </label>
  );
});
Label.displayName = "Label";

export const Select = React.forwardRef(({ className = "", children, ...props }, ref) => {
  return (
    <select
      className={`ui-select ${className}`}
      ref={ref}
      {...props}
    >
      {children}
    </select>
  );
});
Select.displayName = "Select";
