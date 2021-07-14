
def configure_area_det(det,acq_time,exposure,num_exposure=1):
    
    if det.cam.acquire.get() == 0:
        yield from bps.abs_set(det.cam.acquire, 1, wait=True)

    yield from bps.abs_set(det.cam.acquire_time, acq_time, wait=True)
    acq_time = det.cam.acquire_time.get()

    num_frame = np.ceil(exposure / acq_time)
    
    yield from bps.abs_set(det.images_per_set, num_frame, wait=True)
    
    yield from bps.abs_set(det.number_of_sets, num_exposure, wait=True)    

    print("INFO: det = {}; acq_time = {}; exposure = {} (num frame = {}); num_exposure = {}".format(det.name,det.cam.acquire_time.get(),exposure,num_frame,num_exposure))  
    
    
    return 





def set_detector(det,exposure_time=1.0,num_images=1,sleep=0.5):
    if det.name == 'prosilica':
        det.proc.enable_filter.put(0,wait=True)
        det.cam.acquire_time.put(exposure_time)
        det.cam.acquire_period.put(0.5)     
        if num_images > 1:
            print('Multiple mode doesnt work well!!!')
            det.cam.stage_sigs['image_mode'] = 'Multiple'
            det.cam.num_images.put(num_images)
            det.cam.image_mode.put(1)       
        else:
            det.cam.stage_sigs['image_mode'] = 'Single'
            det.cam.num_images.put(1)
            det.cam.image_mode.put(0)
        det.cam.trigger_mode.put(0)
        det.unstage()
        time.sleep(sleep)    
        
    elif det.name == 'blackfly':
        det.proc.enable_filter.put(0,wait=True)
        det.cam.acquire_time.put(exposure_time)    
        det.cam.acquire_period.put(exposure_time)     
        if num_images > 1:
            det.cam.stage_sigs['image_mode'] = 'Multiple'
            det.cam.num_images.put(num_images)
            det.cam.image_mode.put(1)
        else:
            det.cam.stage_sigs['image_mode'] = 'Single'
            det.cam.num_images.put(1)
            det.cam.image_mode.put(0)
        det.cam.trigger_mode.put(0)
        det.unstage()
        time.sleep(sleep)
        
    elif det.name == 'emergent':
        det.proc.enable_filter.put(0,wait=True)
        det.cam.acquire_time.put(exposure_time)
        det.cam.acquire_period.put(exposure_time)             
        if num_images > 1:        
            det.cam.stage_sigs['image_mode'] = 'Multiple'    
            det.cam.stage_sigs['num_images'] = num_images
            det.cam.num_images.put(num_images)  
            det.cam.image_mode.put(1)        
        else:
            det.cam.stage_sigs['image_mode'] = 'Single'
            det.cam.num_images.put(1)
            det.cam.image_mode.put(0)
#         det.cam.trigger_mode.put(0)
        det.unstage()
        time.sleep(sleep)
        
    elif det.name == 'dexela':
        det.proc.enable_filter.put(0,wait=True)
        det.cam.stage_sigs['image_mode'] = 'Multiple'        
        det.cam.stage_sigs['trigger_mode'] = 'Int. Free Run'        
        det.cam.acquire_time.put(exposure_time)
        det.cam.acquire_period.put(exposure_time+0.02)
        if num_images > 1:
            det.cam.stage_sigs['image_mode'] = 'Multiple'
            det.cam.num_images.put(num_images)
            det.cam.image_mode.put(1)
        else:
            det.cam.stage_sigs['image_mode'] = 'Single'
            det.cam.num_images.put(1)
            det.cam.image_mode.put(0)
        det.cam.trigger_mode.put(0)
        det.unstage()
        time.sleep(sleep)

        

        
def beam_on():
    FastShutter.move(-7)
    time.sleep(1)

def beam_off():
    FastShutter.move(-47)
    time.sleep(1)
    
    
        
        
def pud_switcher(ipdu,state='off',sleep=1.0, verbose=False):
    
    pdus = (pdu1,pdu2,pdu3,pdu4)
    
    if state == 'on':
        current_state = pdus[ipdu].value
        if current_state == 1:
            if verbose:
                print('it is already on!')
        else:
            pdus[ipdu].put(1)
            time.sleep(sleep)
    elif state == 'off':
        current_state = pdus[ipdu].value
        if current_state == 0:
            if verbose:
                print('it is already off!')
        else:
            pdus[ipdu].put(0)
            time.sleep(sleep)
            
            

        
        
def get_tiff_list(hdr):

    for name, doc in hdr.documents():       
        if name=='start':
            npts = doc.num_points           
        if name=='resource':
            fpp   = doc.resource_kwargs['frame_per_point'] 
            tpath = os.path.join(doc.root,doc.resource_path)
            fname = doc.resource_kwargs['filename'] 
    tiffs = ['%s/%s_%6.6d.tiff'%(tpath,fname,i) for i in range(npts*fpp)] 
    return tiffs
            
            
            
            
def tiff_cleaner(hdr):

    for name, doc in hdr.documents():       
        if name=='start':
            npts = doc.num_points           
        if name=='resource':
            fpp   = doc.resource_kwargs['frame_per_point'] 
            tpath = os.path.join(doc.root,doc.resource_path)
            fname = doc.resource_kwargs['filename'] 
    tiffs = ['%s/%s_%6.6d.tiff'%(tpath,fname,i) for i in range(npts*fpp)] 
    for t in tiffs:
        os.remove(t)


        
        
        
def read_tiff_as_xarr(tiffpath,
                      figsize=(6,6),
                      robust=True,
                      plot=False,
                      cbar=False,
                      mode = None):

    if mode == 'prosilica':
        img = fabio.open(tiffpath).data
    else:
        img = tifffile.imread(tiffpath).astype('float32')

    da = xr.DataArray(data=img,
                      coords=[np.arange(img.shape[0]),np.arange(img.shape[1])],
                      dims=['pixel_y', 'pixel_x'])

    if plot:

        fig = plt.figure(figsize=figsize)
        ax = fig.add_subplot(1,1,1)

        if not cbar:
            xp = da.plot.imshow(ax=ax,robust=robust,yincrease=False,cmap='Greys_r',
                                add_colorbar=cbar)
        else:
            xp = da.plot.imshow(ax=ax,robust=robust,yincrease=False,cmap='Greys_r',
                                cbar_kwargs=dict( orientation='vertical',
                                            pad=0.07, shrink=0.4, label='Intensity'))            
        xp.axes.set_aspect('equal', 'box')
     
        plt.tight_layout()
        return da
    
    return da
            

    
def print_det_keys(det_class):
    import pprint
    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(det_class.tiff.__dict__)
    
    

    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
def counter(det,exposure_time=1, take_dark=False, take_bright=True, num_dark = 3, num_bright = 2):

    ds = xr.Dataset()

    
    if take_dark:
        set_detector(det,exposure_time=exposure_time,num_images=num_dark)

#         laser_off()
#         light1_off()
#         light2_off()

        beam_off()
        uid_dark = RE(count([det],num=1))[0]
        
        if det.name == 'prosilica':
            tiffs = get_tiff_list(hdr=db[-1])
            t0 = fabio.open(tiffs[0]).data
            img_dark = np.zeros((len(tiffs),t0.shape[0],t0.shape[1]))
            for e,t in enumerate(tiffs):
                img_dark[e,:,:] = fabio.open(tiffs[e]).data
        else:
            img_dark = np.array(list(db[-1].data('%s_image'%(det.name))))
            

        if len(img_dark.shape) == 4:
            img_dark = img_dark.mean(axis=1)
            img_dark = img_dark.mean(axis=0)
        if len(img_dark.shape) == 3:
            img_dark = img_dark.mean(axis=0)
            
        da_dark = xr.DataArray(data=img_dark.astype('float32'),
                  coords=[np.arange(img_dark.shape[0]), np.arange(img_dark.shape[1])],
                  dims=['pixel_y', 'pixel_x'],attrs=None
                 )
        ds['dark'] = da_dark
        dark_taken = 'true'
        
    else:
        uid_dark = 'none'
        num_dark = 'none'
        dark_taken = 'false'

    
    if take_bright:
        beam_on()
        set_detector(det,exposure_time=exposure_time,num_images=num_bright)
        uid_bright = RE(count([det],num=1))[0]
        beam_off()
        bright_taken = 'true'
    else:
        uid_bright = 'none'
        bright_taken = 'false'
        
        
    if bright_taken == 'true':
        if det.name == 'prosilica':
            tiffs = get_tiff_list(hdr=db[-1])
            t0 = fabio.open(tiffs[0]).data
            img_bright = np.zeros((len(tiffs),t0.shape[0],t0.shape[1]))
            for e,t in enumerate(tiffs):
                img_bright[e,:,:] = fabio.open(tiffs[e]).data
        else:
            img_bright = np.array(list(db[-1].data('%s_image'%(det.name))))

        if len(img_bright.shape) == 4:
            img_bright = img_bright.mean(axis=1)
            img_bright = img_bright.mean(axis=0)
        if len(img_bright.shape) == 3:
            img_bright = img_bright.mean(axis=0)


        da_bright = xr.DataArray(data=img_bright.astype('float32'),
                  coords=[np.arange(img_bright.shape[0]), np.arange(img_bright.shape[1])],
                  dims=['pixel_y', 'pixel_x'],attrs=None
                 )
        ds['bright'] = da_bright
        


    md={'type': 'count',
        'time': time.time(),
        'detector':det.name,
        'exposure_time':exposure_time,
        'dark_taken': dark_taken,
        'bright_taken': bright_taken,
        'uid_dark':uid_dark,
        'num_dark':num_dark, 
        'uid_bright':uid_bright,   
        'num_bright':num_bright,    
        'filter1':Filters.flt1.value,
        'filter2':Filters.flt2.value,
        'filter3':Filters.flt3.value,
        'filter4':Filters.flt4.value, 
        'mXBase':mXBase.position,
        'mYBase':mYBase.position,
        'mStackX':mStackX.position,
        'mStackY':mStackY.position, 
        'mStackZ':mStackZ.position,
        'mPhi':mPhi.position,  
        'mSlitsTop':mSlitsTop.position,     
        'mSlitsBottom':mSlitsBottom.position,    
        'mSlitsOutboard':mSlitsOutboard.position,   
        'mSlitsInboard':mSlitsInboard.position,     
        'mPitch':mPitch.position,       
        'mRoll':mRoll.position,      
        'mDexelaPhi':mDexelaPhi.position,       
        'mQuestarX':mQuestarX.position,      
        'mSigrayX':mSigrayX.position,    
        'mSigrayY':mSigrayY.position,    
        'mSigrayZ':mSigrayZ.position,    
        'mSigrayPitch':mSigrayPitch.position,   
        'mSigrayYaw':mSigrayYaw.position,     
        'FastShutter':FastShutter.position,      
       }

    ds.attrs = md
    
    
    return ds






def scanner(det,
            
            exposure_time=0.5, 
            
            take_dark=False, 
            num_dark = 10, 

            
            motor = mStackX,
            motor_start = -0.1,
            motor_stop =  0.1,
            motor_nstep = 11,


           ):

    ds = xr.Dataset()

    
    if take_dark:
        beam_off()
        set_detector(det,exposure_time=exposure_time,num_images=num_dark)
        uid_dark = RE(count([det],num=1))[0]
        
        if det.name == 'prosilica':
            tiffs = get_tiff_list(hdr=db[-1])
            t0 = fabio.open(tiffs[0]).data
            img_dark = np.zeros((len(tiffs),t0.shape[0],t0.shape[1]))
            for e,t in enumerate(tiffs):
                img_dark[e,:,:] = fabio.open(tiffs[e]).data
        else:
            img_dark = np.array(list(db[-1].data('%s_image'%(det.name))))
            
#         tiff_cleaner(hdr=db[-1])
        if len(img_dark.shape) == 4:
            img_dark = img_dark.mean(axis=0)
            img_dark = img_dark.mean(axis=0)
        elif len(img_dark.shape) == 3:
            img_dark = img_dark.mean(axis=0)
            
        da_dark = xr.DataArray(data=img_dark.astype('float32'),
                  coords=[np.arange(img_dark.shape[0]), np.arange(img_dark.shape[1])],
                  dims=['pixel_y', 'pixel_x'],attrs=None
                 )
        ds['dark'] = da_dark
        dark_taken = 'true'
        
    else:
        uid_dark = 'none'
        num_dark = 'none'
        dark_taken = 'false'

    
    beam_on()
    set_detector(det,exposure_time=exposure_time,num_images=1)
    uid_scan = RE(scan([det],motor,motor_start,motor_stop,motor_nstep))[0]
    beam_off()
    
    if det.name == 'prosilica':
        tiffs = get_tiff_list(hdr=db[-1])
        t0 = fabio.open(tiffs[0]).data
        imgs_scan = np.zeros((len(tiffs),t0.shape[0],t0.shape[1]))
        for e,t in enumerate(tiffs):
            imgs_scan[e,:,:] = fabio.open(tiffs[e]).data
    else:
        imgs_scan = np.array(list(db[-1].data('%s_image'%(det.name))))
        
    print(imgs_scan.shape)
    
    if len(imgs_scan.shape) == 4:
        imgs_scan = imgs_scan.mean(axis=1)
        
    motor_pos = np.linspace(motor_start,motor_stop,motor_nstep)
        
#     tiff_cleaner(hdr=db[-1])
   
    da_scan = xr.DataArray(data=imgs_scan.astype('float32'),
              coords=[motor_pos,np.arange(imgs_scan.shape[1]), np.arange(imgs_scan.shape[2])],
              dims=[motor.name,'pixel_y', 'pixel_x'],attrs=None
             )
    ds['scan'] = da_scan


    md={'type': 'scan',
        'time': time.time(),
        'detector':det.name,
        'exposure_time':exposure_time,
        'dark_taken': dark_taken,
        'uid_dark':uid_dark,
        'num_dark':num_dark, 
        'uid_bright':uid_scan,      
        'filter1':Filters.flt1.value,
        'filter2':Filters.flt2.value,
        'filter3':Filters.flt3.value,
        'filter4':Filters.flt4.value, 
        'mXBase':mXBase.position,
        'mYBase':mYBase.position,
        'mStackX':mStackX.position,
        'mStackY':mStackY.position, 
        'mStackZ':mStackZ.position,
        'mPhi':mPhi.position,  
        'mSlitsTop':mSlitsTop.position,     
        'mSlitsBottom':mSlitsBottom.position,    
        'mSlitsOutboard':mSlitsOutboard.position,   
        'mSlitsInboard':mSlitsInboard.position,     
        'mPitch':mPitch.position,       
        'mRoll':mRoll.position,      
        'mDexelaPhi':mDexelaPhi.position,       
        'mQuestarX':mQuestarX.position,      
        'mSigrayX':mSigrayX.position,    
        'mSigrayY':mSigrayY.position,    
        'mSigrayZ':mSigrayZ.position,    
        'mSigrayPitch':mSigrayPitch.position,   
        'mSigrayYaw':mSigrayYaw.position,     
        'FastShutter':FastShutter.position,      
       }

    ds.attrs = md
    
    
    return ds







    
    
def ds_saver(ds,save_to,save_str='_',zlib=False,dtype='float32'):
    comp = dict(zlib=zlib, dtype=dtype)
    encoding = {var: comp for var in ds.data_vars}
    ds.to_netcdf('%s/%d_%s.nc'%(save_to,ds.attrs['time'],save_str), encoding=encoding)    
    
    
    
    
    
    
    
    
    
    
    
    
    
"""           
RE(bps.mv(Filters.flt1, 'Out')) 
RE(bps.mv(Filters.flt2, 'Out'))
RE(bps.mv(Filters.flt3, 'Out'))
RE(bps.mv(Filters.flt4, 'In'))
""" 
