'use client';
import React, { useState, useEffect, Children, cloneElement } from 'react';

const TypingAnimation = ({ children, typingSpeed = 30 }) => {
  const [displayedText, setDisplayedText] = useState('');
  const [cursorPosition, setCursorPosition] = useState({ x: 0, y: 0 });
  const [isTypingComplete, setIsTypingComplete] = useState(false);

  // Function to extract text content from React elements
  const extractTextContent = (element) => {
    if (typeof element === 'string') return element;
    if (!element.props) return '';
    if (typeof element.props.children === 'string') return element.props.children;

    return Children.toArray(element.props.children)
      .map(child => extractTextContent(child))
      .join('');
  };

  // Function to recursively clone and update elements
  const updateTextContent = (element, currentText, textOffset = 0) => {
    if (typeof element === 'string') {
      const text = currentText.slice(textOffset, textOffset + element.length);
      return text;
    }

    if (!element.props) return element;

    if (typeof element.props.children === 'string') {
      const text = currentText.slice(textOffset, textOffset + element.props.children.length);
      return cloneElement(element, { ...element.props, children: text });
    }

    const children = Children.toArray(element.props.children);
    let newOffset = textOffset;

    const newChildren = children.map(child => {
      const updatedChild = updateTextContent(child, currentText, newOffset);
      newOffset += extractTextContent(child).length;
      return updatedChild;
    });

    if (element.type === 'p' || element.type === 'div' || element.type === 'span') {
      // Only add cursor to block or inline elements
      return cloneElement(element, {
        ...element.props,
        children: [...newChildren,
          <span
            key="cursor"
            className={`border-r-2 border-gray-400 ${
              isTypingComplete ? 'animate-pulse' : 'animate-blink'
            }`}
            style={{ marginLeft: '1px' }}
          />
        ]
      });
    }

    return cloneElement(element, { ...element.props, children: newChildren });
  };

  useEffect(() => {
    const fullText = extractTextContent(children);
    let currentIndex = 0;
    let timer;

    const typeNextCharacter = () => {
      if (currentIndex < fullText.length) {
        setDisplayedText(fullText.slice(0, currentIndex + 1));
        currentIndex++;
        timer = setTimeout(typeNextCharacter, typingSpeed);
      } else {
        setIsTypingComplete(true);
      }
    };

    timer = setTimeout(typeNextCharacter, typingSpeed);
    return () => clearTimeout(timer);
  }, [children, typingSpeed]);

  const childrenWithTyping = updateTextContent(children, displayedText);

  return childrenWithTyping;
};

export default TypingAnimation;