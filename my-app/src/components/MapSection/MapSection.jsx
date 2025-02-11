import React, { useState } from 'react';

const MapSection = () => {
  // Состояния для управления параметрами
  const [fullScreen, setFullScreen] = useState(true); 
  const [fullWidth, setFullWidth] = useState(false);
  const [paddingTop, setPaddingTop] = useState(5);
  const [paddingBottom, setPaddingBottom] = useState(5);
  const [borderColor, setBorderColor] = useState('#ACD8AA');
  const [bg, setBg] = useState({
    type: 'color',
    value: '#E9E9E6',
    parallax: false
  });
  const [overlay, setOverlay] = useState(false);
  const [overlayColor, setOverlayColor] = useState('#ffffff');
  const [overlayOpacity, setOverlayOpacity] = useState(0.8);

  // Стили для секции
  const sectionStyle = {
    border: `1px solid ${borderColor}`,
    paddingTop: `${paddingTop}rem`,
    paddingBottom: `${paddingBottom}rem`,
    position: 'relative',
    height: fullScreen ? '100vh' : 'auto',
    width: '100%',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center'
  };

  // Стили для оверлея
  const overlayStyle = {
    backgroundColor: overlayColor,
    opacity: overlayOpacity,
    position: 'absolute',
    top: 0,
    left: 0,
    width: '100%',
    height: '100%'
  };

  return (
    <section 
      className={`map01 ridem5 ${fullScreen ? 'mbr-fullscreen' : ''} ${bg.parallax ? 'mbr-parallax-background' : ''}`}
      style={sectionStyle}
    >
      <div className={fullWidth ? 'container-fluid' : 'container'} style={{ height: '100%', width: '100%' }}>
        <div className="row" style={{ height: '100%', width: '100%' }}>
          <div className="col-12" style={{ height: '100%', width: '100%' }}>
            <div className="content-wrapper" style={{ height: '100%', width: '100%' }}>
              <iframe
                title="Google Map"
                src="https://www.google.com/maps/embed/v1/place?key=AIzaSyCt1265A4qvZy9HKUeA8J15AOC4SrCyZe4&q=Russian%20Federation"
                style={{ width: '100%', height: '100%', border: 0 }}
                allowFullScreen
              />
            </div>
          </div>
        </div>
      </div>
      {overlay && bg.type !== 'color' && (
        <div style={overlayStyle}></div>
      )}
    </section>
  );
};

export default MapSection;