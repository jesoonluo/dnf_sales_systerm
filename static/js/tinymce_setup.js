//For submit articles
tinymce.init({
    selector: '#prew_content',
    directionality:'ltr',
    language:'zh_CN',
    height:400,
    plugins: [
            'advlist lists charmap pagebreak spellchecker',
            'searchreplace visualblocks visualchars fullscreen insertdatetime nonbreaking',
            'save table contextmenu directionality emoticons template textcolor',
    ],
    menu: false,
    menubar:false,
    statusbar: false,
    height: 600,
    readonly: 1,
    toolbar: false,
    fontsize_formats: '10pt 12pt 14pt 18pt 24pt 36pt',
    nonbreaking_force_tab: true
});

tinymce.init({
    selector: '#edit_content',
    directionality:'ltr',
    language:'zh_CN',
    height:400,
    plugins: [
            'advlist lists charmap pagebreak spellchecker',
            'searchreplace visualblocks visualchars fullscreen insertdatetime nonbreaking',
            'save table contextmenu directionality emoticons template textcolor',
    ],
    menu: {},
    toolbar: 'insertfile undo redo | \
     styleselect | \
     bold italic | \
     alignleft aligncenter alignright alignjustify | \
     bullist numlist outdent indent | \
     forecolor backcolor |\
     fontsizeselect fullscreen',
    fontsize_formats: '10pt 12pt 14pt 18pt 24pt 36pt',
    nonbreaking_force_tab: true
});

tinymce.init({
    selector: '#new_content',
    directionality:'ltr',
    language:'zh_CN',
    height:400,
    plugins: [
            'advlist lists charmap pagebreak spellchecker',
            'searchreplace visualblocks visualchars fullscreen insertdatetime nonbreaking',
            'save table contextmenu directionality emoticons template textcolor',
    ],
    menu: {},
    toolbar: 'insertfile undo redo | \
     styleselect | \
     bold italic | \
     alignleft aligncenter alignright alignjustify | \
     bullist numlist outdent indent | \
     forecolor backcolor |\
     fontsizeselect fullscreen',
    fontsize_formats: '10pt 12pt 14pt 18pt 24pt 36pt',
    nonbreaking_force_tab: true
});
